from app import create_app
from app.models.User import User
from flask_wtf.csrf import generate_csrf

def test_register_route(test_client):
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_user(test_client, init_database):
    response = test_client.post(
        "/register",
        data={
            "pseudo": "testuser",
            "email": "test@example.com",
            "password": "Test123!",
            "password_confirmation": "Test123!",
        },
        follow_redirects=True,
    )

    print(response.data)
    assert b"OK !" in response.data

    # # Check if the user has been added to the database
    # with test_client.application.app_context():
    #     user = User.query.filter_by(username='testuser').first()
    #     assert user is not None
    # # You can also check other aspects of the response if needed
    # assert response.status_code == 302  # Redirect status code
    # # assert response.headers["Location"] == "http://localhost/"
