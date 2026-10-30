from app import app


def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"DEVOPS" in response.data
    assert b"PULSE" in response.data


def test_api_health_endpoint():
    response = app.test_client().get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_api_version_endpoint():
    response = app.test_client().get("/api/version")
    assert response.status_code == 200
    data = response.get_json()
    assert data["version"] == "1.0.0"
    assert data["application"] == "DevOps Pulse"


def test_legacy_health_route():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_legacy_version_route():
    response = app.test_client().get("/version")
    assert response.status_code == 200
    assert response.get_json()["version"] == "1.0.0"
