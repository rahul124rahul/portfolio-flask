def test_index_page(client):
    """Test that the public index page loads."""
    response = client.get("/")
    assert response.status_code == 200


def test_contact_post_missing_fields(client):
    """Test contact form with missing fields."""
    response = client.post("/contact", data={"name": "", "email": "", "message": ""})
    assert response.status_code == 302


def test_admin_login_page(client):
    """Test that the admin login page loads."""
    response = client.get("/admin/login")
    assert response.status_code == 200


def test_admin_login_invalid(client):
    """Test login with invalid credentials."""
    response = client.post("/admin/login", data={
        "username": "wrong",
        "password": "wrong",
    })
    assert response.status_code == 200


def test_admin_login_valid(client, admin_user):
    """Test login with valid credentials."""
    response = client.post("/admin/login", data={
        "username": "testadmin",
        "password": "testpass123",
    }, follow_redirects=True)
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    """Test that dashboard redirects to login."""
    response = client.get("/admin/dashboard")
    assert response.status_code == 302


def test_robots_txt(client):
    """Test robots.txt route."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"User-agent" in response.data


def test_sitemap_xml(client):
    """Test sitemap.xml route."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert b"urlset" in response.data
