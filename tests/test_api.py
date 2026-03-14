import json


def test_get_profile_empty(client):
    """Test GET /api/profile when no profile exists."""
    response = client.get("/api/profile")
    assert response.status_code == 404


def test_get_projects_empty(client):
    """Test GET /api/projects with no projects."""
    response = client.get("/api/projects")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []


def test_get_skills_empty(client):
    """Test GET /api/skills with no skills."""
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []


def test_get_experience_empty(client):
    """Test GET /api/experience with no experience."""
    response = client.get("/api/experience")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []


def test_api_login_invalid(client):
    """Test API login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "wrong", "password": "wrong"}),
        content_type="application/json",
    )
    assert response.status_code == 401


def test_api_login_valid(client, admin_user):
    """Test API login with valid credentials."""
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "testadmin", "password": "testpass123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
