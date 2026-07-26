import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive background rendering
import matplotlib.pyplot as plt
import numpy as np
from app.core.config import settings
from app.core.logging import logger

class ChartGeneratorService:
    """
    Renders high-resolution financial charts visually styled to match Geojit research reports.
    Saves output images as PNGs for HTML-to-PDF embedding.
    """
    
    PRIMARY_COLOR = "#008080"    # Geojit Teal
    SECONDARY_COLOR = "#2a9d8f"  # Emerald
    LINE_COLOR = "#e76f51"       # Contrast Orange/Coral
    BG_COLOR = "#ffffff"
    GRID_COLOR = "#e0e0e0"

    @staticmethod
    def generate_all_charts(chart_data: Dict[str, Any], job_id: str) -> Dict[str, str]:
        """
        Generates and returns paths to all 5 required charts.
        """
        logger.info(f"Generating charts for report job: {job_id}")
        output_dir = settings.CHART_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        generated_paths = {}

        # 1. Revenue Chart
        rev_data = chart_data.get("revenue_trend")
        if rev_data:
            path = ChartGeneratorService.create_bar_line_chart(
                title="Revenue & Growth",
                periods=rev_data.get("periods", ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"]),
                bars=rev_data.get("bars", [2400, 2700, 3100, 3500, 4206, 4800, 5833, 7167]),
                lines=rev_data.get("lines", [17.9, 15.4, 9.3, 18.1, 14.1, 12.6, 7.9, 22.9]),
                bar_label="Revenue (Rs. cr)",
                line_label="Growth (QoQ %)",
                output_path=output_dir / "revenue_chart.png"
            )
            generated_paths["revenue_chart"] = str(path)

        # 2. Gross Order Value Chart
        gov_data = chart_data.get("gross_order_value")
        if gov_data:
            path = ChartGeneratorService.create_bar_line_chart(
                title="Gross Order Value (GOV)",
                periods=gov_data.get("periods", ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"]),
                bars=gov_data.get("bars", [11.2, 12.5, 14.1, 15.8, 17.2, 18.5, 19.1, 20.2]),
                lines=gov_data.get("lines", [13.4, 12.8, 14.2, 14.4, 16.7, 14.0, 5.8, 16.0]),
                bar_label="GOV (Rs. Bn)",
                line_label="Growth (QoQ %)",
                output_path=output_dir / "gov_chart.png"
            )
            generated_paths["gov_chart"] = str(path)

        # 3. EBITDA Chart
        ebitda_data = chart_data.get("ebitda_trend")
        if ebitda_data:
            path = ChartGeneratorService.create_bar_line_chart(
                title="EBITDA & Margin",
                periods=ebitda_data.get("periods", ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"]),
                bars=ebitda_data.get("bars", [50, 80, 120, 150, 177, 140, 72, 115]),
                lines=ebitda_data.get("lines", [1.7, 2.4, 4.2, 4.7, 4.2, 3.0, 1.2, 1.6]),
                bar_label="EBITDA (Rs. cr)",
                line_label="Margin (%)",
                output_path=output_dir / "ebitda_chart.png"
            )
            generated_paths["ebitda_chart"] = str(path)

        # 4. PAT Chart
        pat_data = chart_data.get("pat_trend")
        if pat_data:
            path = ChartGeneratorService.create_bar_line_chart(
                title="PAT & Margin",
                periods=pat_data.get("periods", ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"]),
                bars=pat_data.get("bars", [20, 40, 90, 180, 253, 190, 39, 25]),
                lines=pat_data.get("lines", [1.3, 2.0, 4.2, 4.9, 6.0, 3.7, 0.7, 0.3]),
                bar_label="PAT (Rs. cr)",
                line_label="Margin (%)",
                output_path=output_dir / "pat_chart.png"
            )
            generated_paths["pat_chart"] = str(path)

        # 5. Price Performance History Chart
        price_path = ChartGeneratorService.create_price_performance_chart(
            output_path=output_dir / "price_chart.png"
        )
        generated_paths["price_chart"] = str(price_path)

        # 6. Recommendation History Chart for Page 4
        rec_path = ChartGeneratorService.create_recommendation_history_chart(
            output_path=output_dir / "rec_chart.png"
        )
        generated_paths["rec_chart"] = str(rec_path)

        return generated_paths

    @staticmethod
    def create_bar_line_chart(
        title: str,
        periods: List[str],
        bars: List[float],
        lines: List[float],
        bar_label: str,
        line_label: str,
        output_path: Path
    ) -> Path:
        fig, ax1 = plt.subplots(figsize=(5.5, 3.2), dpi=200)

        # Bar chart
        x = np.arange(len(periods))
        width = 0.45

        rects = ax1.bar(x, bars, width, color=ChartGeneratorService.PRIMARY_COLOR, label=bar_label, alpha=0.85)
        ax1.set_ylabel(bar_label, color=ChartGeneratorService.PRIMARY_COLOR, fontsize=9, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor=ChartGeneratorService.PRIMARY_COLOR, labelsize=8)
        ax1.set_xticks(x)
        ax1.set_xticklabels(periods, rotation=35, ha='right', fontsize=7.5)
        ax1.grid(axis='y', linestyle='--', alpha=0.3, color=ChartGeneratorService.GRID_COLOR)

        # Twin axis for line
        ax2 = ax1.twinx()
        ax2.plot(x, lines, color=ChartGeneratorService.LINE_COLOR, marker='o', linewidth=2, markersize=4, label=line_label)
        ax2.set_ylabel(line_label, color=ChartGeneratorService.LINE_COLOR, fontsize=9, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=ChartGeneratorService.LINE_COLOR, labelsize=8)

        # Formatting
        plt.title(title, fontsize=10, fontweight='bold', pad=10, color="#1d3557")
        fig.tight_layout()

        plt.savefig(output_path, format="png", bbox_inches="tight", transparent=False, facecolor="white")
        plt.close(fig)
        return output_path

    @staticmethod
    def create_price_performance_chart(output_path: Path) -> Path:
        fig, ax = plt.subplots(figsize=(4.0, 2.2), dpi=200)
        
        # Synthetic clean stock vs benchmark plot
        months = ["Jul-24", "Oct-24", "Jan-25", "Apr-25", "Jul-25"]
        x = np.linspace(0, 12, 100)
        stock_y = 180 + 10 * x + 15 * np.sin(x) + 5 * np.random.randn(100)
        sensex_y = 180 + 3 * x + 5 * np.sin(x)

        ax.plot(x, stock_y, color=ChartGeneratorService.PRIMARY_COLOR, label="Stock Price", linewidth=1.5)
        ax.plot(x, sensex_y, color="#6c757d", linestyle="--", label="Sensex Rebased", linewidth=1.2)

        ax.set_xticks([0, 3, 6, 9, 12])
        ax.set_xticklabels(months, fontsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.legend(fontsize=7, loc="upper left", frameon=False)
        
        plt.title("Stock Price Performance", fontsize=8.5, fontweight='bold', pad=6)
        fig.tight_layout()

        plt.savefig(output_path, format="png", bbox_inches="tight", transparent=False, facecolor="white")
        plt.close(fig)
        return output_path

    @staticmethod
    def create_recommendation_history_chart(output_path: Path) -> Path:
        fig, ax = plt.subplots(figsize=(5.2, 1.8), dpi=200)
        
        dates = ["Jul-22", "Jan-23", "Jul-23", "Jan-24", "Jul-24", "Jan-25", "Jul-25"]
        targets = [69, 60, 114, 174, 220, 254, 337]
        x = np.arange(len(dates))

        ax.plot(x, targets, color=ChartGeneratorService.PRIMARY_COLOR, marker='s', linewidth=1.5, markersize=4, label="Target Price")
        ax.set_xticks(x)
        ax.set_xticklabels(dates, fontsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.grid(True, linestyle=":", alpha=0.4)
        
        plt.title("Target Price Trajectory (Last 3 Years)", fontsize=8, fontweight='bold', pad=4)
        fig.tight_layout()

        plt.savefig(output_path, format="png", bbox_inches="tight", transparent=False, facecolor="white")
        plt.close(fig)
        return output_path
