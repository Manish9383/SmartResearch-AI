import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.api.endpoints import router as api_router

setup_logging()
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and output directories
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
app.mount("/reports", StaticFiles(directory=str(settings.REPORT_DIR)), name="reports")

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Financial Research Report Generator API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
