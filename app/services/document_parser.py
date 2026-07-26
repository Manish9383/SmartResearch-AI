import os
import re
from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from typing import Dict, Any, List
from app.core.logging import logger

class DocumentParserService:
    """
    Extracts text, structured tables, and partition sections from PDF, TXT, and CSV documents
    for ingestion by specialized AI Agents.
    """
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found at {file_path}")
            
        ext = path.suffix.lower()
        if ext == ".pdf":
            parsed = DocumentParserService._parse_pdf(file_path)
        elif ext in [".txt", ".text"]:
            parsed = DocumentParserService._parse_txt(file_path)
        elif ext == ".csv":
            parsed = DocumentParserService._parse_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        # Perform section detection across extracted text
        parsed["sections"] = DocumentParserService.detect_sections(parsed["combined_content"])
        return parsed

    @staticmethod
    def detect_sections(full_content: str) -> Dict[str, str]:
        """
        Detects and extracts document sections (Company Info, Quarterly Results, Financial Tables, Management Commentary, Risks & Outlook).
        """
        sections = {
            "company_info": "",
            "quarterly_performance": "",
            "financial_tables": "",
            "management_commentary": "",
            "risks_and_outlook": ""
        }

        lines = full_content.split("\n")
        current_section = "company_info"
        buffer: Dict[str, List[str]] = {sec: [] for sec in sections.keys()}

        for line in lines:
            line_lower = line.lower()
            if any(k in line_lower for k in ["quarterly", "q1", "q2", "q3", "q4", "result update", "financial highlights"]):
                current_section = "quarterly_performance"
            elif any(k in line_lower for k in ["balance sheet", "profit & loss", "profit and loss", "cashflow", "consolidated financials", "ratio"]):
                current_section = "financial_tables"
            elif any(k in line_lower for k in ["management commentary", "concall", "earnings call", "transcript", "remarks", "highlights"]):
                current_section = "management_commentary"
            elif any(k in line_lower for k in ["risk", "outlook", "guidance", "threats", "valuation"]):
                current_section = "risks_and_outlook"

            buffer[current_section].append(line)

        for sec in sections.keys():
            sections[sec] = "\n".join(buffer[sec]).strip()

        return sections

    @staticmethod
    def _parse_pdf(file_path: str) -> Dict[str, Any]:
        logger.info(f"Parsing PDF document: {file_path}")
        text_content = []
        tables_content = []

        # 1. PyMuPDF for fast, robust text extraction
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text("text")
            if page_text.strip():
                text_content.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
        doc.close()

        # 2. pdfplumber for table extraction
        try:
            with pdfplumber.open(file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    extracted_tables = page.extract_tables()
                    for t_idx, table in enumerate(extracted_tables):
                        if table:
                            df = pd.DataFrame(table)
                            tables_content.append(
                                f"### Page {idx+1} Table {t_idx+1}\n" + df.to_markdown(index=False)
                            )
        except Exception as e:
            logger.warning(f"pdfplumber table extraction warning: {e}")

        full_text = "\n\n".join(text_content)
        full_tables = "\n\n".join(tables_content)

        return {
            "file_type": "pdf",
            "text": full_text,
            "tables_text": full_tables,
            "combined_content": f"DOCUMENT TEXT:\n{full_text}\n\nDOCUMENT TABLES:\n{full_tables}"
        }

    @staticmethod
    def _parse_txt(file_path: str) -> Dict[str, Any]:
        logger.info(f"Parsing TXT document: {file_path}")
        encodings = ["utf-8", "latin-1", "cp1252"]
        content = ""
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        return {
            "file_type": "txt",
            "text": content,
            "tables_text": "",
            "combined_content": content
        }

    @staticmethod
    def _parse_csv(file_path: str) -> Dict[str, Any]:
        logger.info(f"Parsing CSV document: {file_path}")
        df = pd.read_csv(file_path)
        markdown_table = df.to_markdown(index=False)
        summary = f"CSV Data ({len(df)} rows, {len(df.columns)} columns):\nColumns: {', '.join(df.columns)}\n\n{markdown_table}"
        
        return {
            "file_type": "csv",
            "text": summary,
            "tables_text": markdown_table,
            "combined_content": summary
        }

