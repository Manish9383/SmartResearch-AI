import os
import uuid
import shutil
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db, init_db
from app.models.report_model import DocumentModel, ReportJobModel
from app.services.report_pipeline import ReportPipelineService

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads document (PDF, TXT, CSV) and creates document record.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".txt", ".csv"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Supported: .pdf, .txt, .csv")

    doc_id = str(uuid.uuid4())
    save_filename = f"{doc_id}_{file.filename}"
    save_path = settings.UPLOAD_DIR / save_filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = DocumentModel(
        id=doc_id,
        filename=file.filename,
        file_path=str(save_path),
        file_type=ext.replace(".", "")
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "message": "File uploaded successfully"
    }

@router.post("/generate-report")
async def generate_report(
    background_tasks: BackgroundTasks,
    document_id: str = Form(...),
    company_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Initiates asynchronous financial research report generation.
    """
    doc = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    job_id = str(uuid.uuid4())
    job = ReportJobModel(
        id=job_id,
        document_id=doc.id,
        company_name=company_name or doc.filename,
        status="PENDING",
        progress=0.05,
        current_step="Queued for analysis"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Launch processing task in background thread
    background_tasks.add_task(
        ReportPipelineService.process_report_job,
        job_id=job_id,
        file_path=doc.file_path,
        company_name_override=company_name
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "message": "Report generation initiated"
    }

@router.get("/report/{id}")
def get_report_status(id: str, db: Session = Depends(get_db)):
    """
    Returns current report status, progress percentage, and structured report JSON when complete.
    """
    job = db.query(ReportJobModel).filter(ReportJobModel.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Report job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "current_step": job.current_step,
        "structured_json": job.structured_json,
        "pdf_download_url": f"{settings.API_V1_STR}/download/{job.id}" if job.status == "COMPLETED" else None,
        "error_message": job.error_message,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None
    }

@router.get("/preview/{id}")
def preview_pdf_report(id: str, db: Session = Depends(get_db)):
    """
    Renders the generated PDF research report inline inside an iframe.
    """
    job = db.query(ReportJobModel).filter(ReportJobModel.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Report job not found")

    if job.status != "COMPLETED" or not job.pdf_path or not os.path.exists(job.pdf_path):
        raise HTTPException(status_code=400, detail="PDF report is not ready or failed to generate.")

    return FileResponse(
        path=job.pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline"}
    )

@router.get("/download/{id}")
def download_pdf_report(id: str, db: Session = Depends(get_db)):
    """
    Downloads the generated PDF research report.
    """
    job = db.query(ReportJobModel).filter(ReportJobModel.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Report job not found")

    if job.status != "COMPLETED" or not job.pdf_path or not os.path.exists(job.pdf_path):
        raise HTTPException(status_code=400, detail="PDF report is not ready or failed to generate.")

    return FileResponse(
        path=job.pdf_path,
        media_type="application/pdf",
        filename=f"Geojit_Research_Report_{job.company_name or 'Financial'}.pdf"
    )


@router.get("/reports")
def list_reports(db: Session = Depends(get_db)):
    """
    Lists all generated research reports.
    """
    jobs = db.query(ReportJobModel).order_by(ReportJobModel.created_at.desc()).all()
    return [
        {
            "job_id": j.id,
            "company_name": j.company_name,
            "status": j.status,
            "progress": j.progress,
            "created_at": j.created_at.isoformat()
        } for j in jobs
    ]
