import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Financial Research Report Generator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Storage Paths
    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = BASE_DIR / "app" / "uploads"
    CHART_DIR: Path = BASE_DIR / "app" / "charts"
    REPORT_DIR: Path = BASE_DIR / "app" / "generated_reports"
    TEMPLATE_DIR: Path = BASE_DIR / "app" / "templates"
    STATIC_DIR: Path = BASE_DIR / "app" / "static"
    
    # LLM & AI Settings
    GEMINI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gemini-2.5-flash"
    
    # Database & Redis Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./financial_reports.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

# Ensure required directories exist
for path in [settings.UPLOAD_DIR, settings.CHART_DIR, settings.REPORT_DIR, settings.TEMPLATE_DIR, settings.STATIC_DIR]:
    path.mkdir(parents=True, exist_ok=True)
