import datetime
import uuid
from typing import Optional
from sqlalchemy import String, Text, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)  # pdf, txt, csv
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

class ReportJobModel(Base):
    __tablename__ = "report_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(String, ForeignKey("documents.id"), nullable=False)
    company_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    current_step: Mapped[str] = mapped_column(String, default="Initiated")
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    structured_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    pdf_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
