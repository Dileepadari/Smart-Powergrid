from gridwatch import db


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_and_logout(client, auth):
    response = auth.login()
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert b"Resident1" in dashboard.data

    auth.logout()
    assert client.get("/").status_code == 302


def test_login_rejects_a_bad_password(client, auth):
    response = auth.login(password="nope")
    assert response.status_code == 200
    assert b"not recognised" in response.data


def test_login_next_parameter_cannot_leave_the_site(client):
    response = client.post(
        "/login?next=https://evil.example.com",
        data={"email": "Resident1@students.iiit.ac.in", "password": "password1"},
    )
    assert response.headers["Location"] == "/"


def test_passwords_are_never_stored_in_the_clear(app):
    with app.app_context():
        row = db.query_one("SELECT password_hash FROM users WHERE username = 'Resident1'")
        assert "password1" not in row["password_hash"]
        assert row["password_hash"].startswith(("pbkdf2:", "scrypt:"))


def test_signup_creates_an_account(client):
    response = client.post(
        "/signup",
        data={
            "username": "newcomer",
            "email": "new@example.com",
            "password": "a-long-password",
            "confirm": "a-long-password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Add your appliances" in response.data


def test_signup_rejects_a_duplicate_email(client):
    response = client.post(
        "/signup",
        data={
            "username": "another",
            "email": "Resident1@students.iiit.ac.in",
            "password": "a-long-password",
            "confirm": "a-long-password",
        },
    )
    assert b"already exists" in response.data


def test_admin_pages_are_closed_to_residents(client, auth):
    auth.login()
    response = client.get("/admin", follow_redirects=True)
    assert b"for administrators" in response.data


def test_admin_can_see_the_resident_overview(client, auth):
    auth.login_admin()
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Resident1" in response.data
    assert b"Resident2" in response.data
