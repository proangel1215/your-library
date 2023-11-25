# from app.models.User import User
# from app.forms import RegisterForm


def test_login_route(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data