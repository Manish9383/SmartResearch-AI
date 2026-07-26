import os
import pytest
from app.services.document_parser import DocumentParserService

def test_txt_parser(tmp_path):
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Company XYZ Q1 Results. Revenue surged 25% YoY to Rs. 5000 cr.")
    
    parsed = DocumentParserService.parse_file(str(txt_file))
    assert parsed["file_type"] == "txt"
    assert "Revenue surged 25%" in parsed["text"]

def test_csv_parser(tmp_path):
    csv_file = tmp_path / "financials.csv"
    csv_file.write_text("Quarter,Revenue,PAT\nQ1,5000,500\nQ2,5500,580\n")
    
    parsed = DocumentParserService.parse_file(str(csv_file))
    assert parsed["file_type"] == "csv"
    assert "Revenue" in parsed["text"]
    assert "5500" in parsed["text"]
