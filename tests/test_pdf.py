import os
from pathlib import Path
import pytest
from app.services.chart_generator import ChartGeneratorService
from app.services.pdf_generator import PDFGeneratorService
from app.services.llm_extractor import LLMExtractionService

def test_chart_generation(tmp_path):
    sample_data = LLMExtractionService.extract_structured_data("Test text", "Test Co")
    charts = ChartGeneratorService.generate_all_charts(sample_data["chart_data"], "test_job_123")
    
    assert "revenue_chart" in charts
    assert Path(charts["revenue_chart"]).exists()

def test_pdf_generation(tmp_path):
    sample_data = LLMExtractionService.extract_structured_data("Test text", "Test Co")
    charts = ChartGeneratorService.generate_all_charts(sample_data["chart_data"], "test_job_456")
    
    pdf_path = PDFGeneratorService.generate_pdf(sample_data, charts, "test_job_456")
    assert Path(pdf_path).exists()
    assert os.path.getsize(pdf_path) > 0
