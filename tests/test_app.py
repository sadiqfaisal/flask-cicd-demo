from app import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevOps CI/CD Dashboard" in response.data

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_version_endpoint():
    client = app.test_client()
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"
