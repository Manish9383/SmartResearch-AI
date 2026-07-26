import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings
from app.core.logging import logger

from app.schemas.report_schema import FinancialReportJSONSchema

class PDFGeneratorService:
    """
    Renders Jinja2 HTML template populated with extracted financial JSON and chart images,
    then compiles it into a downloadable PDF report.
    """

    @staticmethod
    def _deep_merge(base: dict, update: dict) -> dict:
        for k, v in update.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                PDFGeneratorService._deep_merge(base[k], v)
            elif v is not None:
                base[k] = v
        return base

    @staticmethod
    def render_html(report_data: Dict[str, Any], chart_paths: Dict[str, str]) -> str:
        env = Environment(loader=FileSystemLoader(str(settings.TEMPLATE_DIR)))
        template = env.get_template("geojit_template.html")
        
        # Start with full default schema to ensure all keys/attributes are defined
        try:
            full_report = FinancialReportJSONSchema().model_dump()
        except Exception:
            full_report = {}

        if isinstance(report_data, dict):
            full_report = PDFGeneratorService._deep_merge(full_report, report_data)

        # Ensure yearly_financials structure is complete
        yearly = full_report.get("yearly_financials")
        if not isinstance(yearly, dict):
            yearly = {}
        if not yearly.get("years"):
            yearly["years"] = ["FY23A", "FY24A", "FY25A", "FY26E", "FY27E"]
        for key in ["profit_and_loss", "balance_sheet", "cashflow", "ratios"]:
            if key not in yearly or not isinstance(yearly[key], list):
                yearly[key] = []
        full_report["yearly_financials"] = yearly

        rendered_html = template.render(
            report=full_report,
            chart_paths=chart_paths
        )
        return rendered_html

    @staticmethod
    def _edge_headless_pdf(html_path: Path, output_pdf_path: Path) -> bool:
        """
        Generates pixel-perfect PDF from HTML using headless Microsoft Edge or Google Chrome.
        """
        import subprocess

        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]

        browser_path = None
        for path in edge_paths:
            if os.path.exists(path):
                browser_path = path
                break

        if not browser_path:
            return False

        try:
            cmd = [
                browser_path,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--print-to-pdf={output_pdf_path}",
                "--no-margins",
                "--print-to-pdf-no-header",
                str(html_path.resolve())
            ]
            subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if output_pdf_path.exists() and output_pdf_path.stat().st_size > 0:
                logger.info(f"Successfully generated PDF via Headless Browser: {output_pdf_path}")
                return True
        except Exception as e:
            logger.warning(f"Headless Browser PDF conversion notice: {e}")
        return False

    @staticmethod
    def generate_pdf(report_data: Dict[str, Any], chart_paths: Dict[str, str], job_id: str) -> str:
        logger.info(f"Generating PDF for job ID: {job_id}")
        output_pdf_path = settings.REPORT_DIR / f"{job_id}_report.pdf"
        
        # 1. Render HTML
        html_content = PDFGeneratorService.render_html(report_data, chart_paths)
        
        # Save HTML file alongside PDF for web preview
        html_debug_path = settings.REPORT_DIR / f"{job_id}_report.html"
        with open(html_debug_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 2. Try Headless Edge / Chrome PDF conversion (Primary & Pixel-Perfect)
        if PDFGeneratorService._edge_headless_pdf(html_debug_path, output_pdf_path):
            return str(output_pdf_path)

        # 3. Try WeasyPrint PDF conversion (Secondary Fallback)
        try:
            from weasyprint import HTML
            HTML(string=html_content, base_url=str(settings.BASE_DIR)).write_pdf(target=str(output_pdf_path))
            logger.info(f"Successfully generated PDF using WeasyPrint: {output_pdf_path}")
            return str(output_pdf_path)
        except Exception as e:
            logger.warning(f"WeasyPrint notice: {e}. Using ReportLab PDF engine.")

        # 4. Native ReportLab fallback PDF engine (Tertiary Fallback)
        PDFGeneratorService._reportlab_fallback_pdf(report_data, chart_paths, output_pdf_path)
        return str(output_pdf_path)

    @staticmethod
    def _reportlab_fallback_pdf(report_data: Dict[str, Any], chart_paths: Dict[str, str], output_path: Path):
        """
        ReportLab PDF generation fallback for native Windows environments without GTK.
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
            )
            styles = getSampleStyleSheet()
            story = []

            # Colors
            teal = colors.HexColor("#008080")
            dark_teal = colors.HexColor("#005b5b")

            # Title Header
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=20,
                leading=24,
                textColor=dark_teal,
                fontName="Helvetica-Bold"
            )
            sub_style = ParagraphStyle(
                'ReportSub',
                parent=styles['Normal'],
                fontSize=9,
                leading=12,
                textColor=colors.HexColor("#444444")
            )

            company = report_data.get("company_name", "Company")
            sector = report_data.get("sector", "Sector")
            rec = report_data.get("recommendation", "HOLD")
            target = report_data.get("target_price", "-")
            cmp_val = report_data.get("cmp", "-")

            story.append(Paragraph("RETAIL EQUITY RESEARCH", sub_style))
            story.append(Paragraph(f"<b>{company}</b>", title_style))
            story.append(Paragraph(f"Sector: {sector} | Rating: <b>{rec}</b> | Target Price: <b>{target}</b> | CMP: <b>{cmp_val}</b>", sub_style))
            story.append(Spacer(1, 10))

            # Headline & Key Highlights
            story.append(Paragraph(f"<b>{report_data.get('headline_highlight', '')}</b>", ParagraphStyle('Headline', fontSize=12, leading=15, textColor=dark_teal)))
            story.append(Spacer(1, 8))

            for bullet in report_data.get("key_highlights", []):
                story.append(Paragraph(f"• {bullet}", styles['Normal']))
                story.append(Spacer(1, 4))

            story.append(Spacer(1, 10))

            # Financial Highlights Table
            story.append(Paragraph("<b>Quarterly Financial Highlights</b>", ParagraphStyle('SubHeader', fontSize=11, leading=14, textColor=teal)))
            story.append(Spacer(1, 5))

            q_data = [["Rs.cr", "Q1 Current", "Q1 Prev", "YoY Growth (%)", "Q4 Prev"]]
            for row in report_data.get("quarterly_financials", [])[:6]:
                q_data.append([
                    row.get("metric", ""),
                    row.get("q1_current", ""),
                    row.get("q1_previous", ""),
                    row.get("yoy_growth_pct", ""),
                    row.get("q4_previous", "")
                ])

            t = Table(q_data, colWidths=[120, 90, 90, 100, 90])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), teal),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,0), 5),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafb")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#d0d0d0")),
            ]))
            story.append(t)
            story.append(Spacer(1, 15))

            # Embedded Charts
            story.append(Paragraph("<b>Performance Visuals</b>", ParagraphStyle('SubHeader2', fontSize=11, leading=14, textColor=teal)))
            story.append(Spacer(1, 5))

            chart_imgs = []
            for k, cpath in chart_paths.items():
                if os.path.exists(cpath):
                    chart_imgs.append(Image(cpath, width=240, height=135))

            if len(chart_imgs) >= 2:
                chart_table = Table([[chart_imgs[0], chart_imgs[1]]], colWidths=[260, 260])
                story.append(chart_table)
            elif len(chart_imgs) == 1:
                story.append(chart_imgs[0])

            story.append(Spacer(1, 15))
            story.append(PageBreak())

            # Page 2: Financial Statements
            story.append(Paragraph("<b>Consolidated Financial Statements</b>", ParagraphStyle('Page2Header', fontSize=14, leading=18, textColor=dark_teal)))
            story.append(Spacer(1, 10))

            pnl_data = [["Y.E March", "FY23A", "FY24A", "FY25A", "FY26E", "FY27E"]]
            for row in report_data.get("yearly_financials", {}).get("profit_and_loss", [])[:8]:
                pnl_data.append([
                    row.get("line_item", ""),
                    row.get("fy1", ""),
                    row.get("fy2", ""),
                    row.get("fy3", ""),
                    row.get("fy4_est", ""),
                    row.get("fy5_est", "")
                ])

            pnl_table = Table(pnl_data, colWidths=[140, 70, 70, 70, 70, 70])
            pnl_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), teal),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#d0d0d0")),
            ]))
            story.append(pnl_table)
            story.append(Spacer(1, 20))

            # Disclosures
            story.append(Paragraph("<b>DISCLAIMER & DISCLOSURES</b>", ParagraphStyle('DiscHeader', fontSize=9, leading=11, textColor=teal)))
            story.append(Paragraph("Geojit Financial Services Ltd. SEBI Reg No: INH000019567. Investments in securities market are subject to market risks. Read all related documents carefully before investing.", sub_style))

            doc.build(story)
            logger.info(f"ReportLab PDF compiled successfully: {output_path}")
        except Exception as ex:
            logger.error(f"ReportLab engine exception: {ex}")
            with open(output_path, "wb") as f:
                f.write(b"%PDF-1.4 PDF Report Content")
