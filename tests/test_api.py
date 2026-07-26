from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_upload_and_generate(tmp_path):
    # Upload TXT file
    files = {"file": ("test_company.txt", b"Company XYZ Q1 Revenue 1000 cr PAT 100 cr", "text/plain")}
    res_upload = client.post("/api/v1/upload", files=files)
    assert res_upload.status_code == 200
    doc_id = res_upload.json()["document_id"]
    
    # Trigger report generation
    res_gen = client.post("/api/v1/generate-report", data={"document_id": doc_id, "company_name": "Test XYZ Ltd"})
    assert res_gen.status_code == 200
    job_id = res_gen.json()["job_id"]
    
    # Check status
    res_status = client.get(f"/api/v1/report/{job_id}")
    assert res_status.status_code == 200
    assert res_status.json()["job_id"] == job_id
