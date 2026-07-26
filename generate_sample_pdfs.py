import os
from app.services.llm_extractor import LLMExtractionService
from app.services.chart_generator import ChartGeneratorService
from app.services.pdf_generator import PDFGeneratorService
from app.core.config import settings

def generate_samples():
    print("Generating Sample PDF #1: Eternal Ltd. (Zomato)...")
    data_1 = LLMExtractionService.extract_structured_data(
        document_content="Eternal Ltd. Q1FY26 revenue surged 70.4% YoY to Rs 7,167cr. Blinkit quick commerce revenue grew 154.8% YoY.",
        company_name_override="Eternal Ltd."
    )
    data_1["sector"] = "Internet & Catalogue Retail"
    data_1["recommendation"] = "HOLD"
    data_1["target_price"] = "Rs. 337"
    data_1["cmp"] = "Rs. 306"
    data_1["return_pct"] = "+10%"
    
    charts_1 = ChartGeneratorService.generate_all_charts(data_1["chart_data"], "sample_eternal_ltd")
    pdf_path_1 = PDFGeneratorService.generate_pdf(data_1, charts_1, "sample_eternal_ltd")
    print(f"Sample 1 Generated: {pdf_path_1}")

    print("Generating Sample PDF #2: Pondy Oxides and Chemicals (POCL)...")
    data_2 = LLMExtractionService.extract_structured_data(
        document_content="POCL Q2FY26 revenue increased to Rs. 6,345 Mn up 11% YoY. EBITDA and PAT increased by 84% & 105%.",
        company_name_override="Pondy Oxides & Chemicals Ltd (POCL)"
    )
    data_2["sector"] = "Chemicals & Metal Recycling"
    data_2["recommendation"] = "BUY"
    data_2["target_price"] = "Rs. 1,650"
    data_2["cmp"] = "Rs. 1,370"
    data_2["return_pct"] = "+20.4%"
    
    charts_2 = ChartGeneratorService.generate_all_charts(data_2["chart_data"], "sample_pocl")
    pdf_path_2 = PDFGeneratorService.generate_pdf(data_2, charts_2, "sample_pocl")
    print(f"Sample 2 Generated: {pdf_path_2}")

if __name__ == "__main__":
    generate_samples()

