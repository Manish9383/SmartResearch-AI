import os
import time
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.database import SessionLocal
from app.models.report_model import ReportJobModel
from app.services.document_parser import DocumentParserService
from app.services.llm_extractor import LLMExtractionService
from app.services.chart_generator import ChartGeneratorService
from app.services.pdf_generator import PDFGeneratorService

class ReportPipelineService:
    """
    Orchestrates the complete workflow:
    1. Parse uploaded document (PDF/TXT/CSV)
    2. Extract structured JSON via LLM
    3. Generate high-res trend charts
    4. Render Jinja2 template into PDF
    5. Update job status in database
    """

    @staticmethod
    def process_report_job(job_id: str, file_path: str, company_name_override: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"Starting Report Pipeline Execution for Job {job_id}")
        db = SessionLocal()
        job = db.query(ReportJobModel).filter(ReportJobModel.id == job_id).first()

        try:
            # Step 1: Document Text & Table Extraction (20%)
            ReportPipelineService._update_job(db, job, "PROCESSING", 0.20, "Extracting text and tables from document...")
            parsed_doc = DocumentParserService.parse_file(file_path)

            # Step 2: Multi-Agent AI Financial Extraction & Structuring (50%)
            ReportPipelineService._update_job(db, job, "PROCESSING", 0.50, "Executing 8-Stage AI Agent Pipeline (Company Profile, Metrics, Thesis, Risks, Financials)...")
            structured_json = LLMExtractionService.extract_structured_data(
                document_content=parsed_doc["combined_content"],
                company_name_override=company_name_override,
                parsed_doc=parsed_doc
            )

            # Step 3: Generating Financial Charts (75%)
            ReportPipelineService._update_job(db, job, "PROCESSING", 0.75, "Generating financial trend charts & visuals...")
            chart_paths = ChartGeneratorService.generate_all_charts(
                chart_data=structured_json.get("chart_data", {}),
                job_id=job_id
            )

            # Step 4: Compiling Geojit PDF Template (90%)
            ReportPipelineService._update_job(db, job, "PROCESSING", 0.90, "Filling HTML template & compiling final PDF report...")
            pdf_path = PDFGeneratorService.generate_pdf(
                report_data=structured_json,
                chart_paths=chart_paths,
                job_id=job_id
            )

            # Step 5: Completion (100%)
            job.status = "COMPLETED"
            job.progress = 1.0
            job.current_step = "Report generation complete"
            job.extracted_text = parsed_doc["combined_content"][:5000]
            job.structured_json = structured_json
            job.pdf_path = pdf_path
            db.commit()

            logger.info(f"Report Job {job_id} COMPLETED successfully. PDF: {pdf_path}")
            return {
                "job_id": job_id,
                "status": "COMPLETED",
                "pdf_path": pdf_path,
                "structured_json": structured_json
            }

        except Exception as e:
            logger.error(f"Error in processing report job {job_id}: {e}", exc_info=True)
            if job:
                job.status = "FAILED"
                job.error_message = str(e)
                job.current_step = "Failed during report generation"
                db.commit()
            raise e
        finally:
            db.close()

    @staticmethod
    def _update_job(db, job: ReportJobModel, status: str, progress: float, current_step: str):
        if job:
            job.status = status
            job.progress = progress
            job.current_step = current_step
            db.commit()
            db.refresh(job)
