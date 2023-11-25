from app.models.User import User
from app.forms import RegisterForm


def test_register_route(test_client):
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_user_success(test_client, init_database):

    form = RegisterForm(email="test52@example.com", pseudo="testuser", password="Test123!", password_confirmation="Test123!")

    response = test_client.post("/register", data=form.data)

    # Check if the user has been added to the database
    with test_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None

    # Check for successful registration flash message and redirection
    assert b"home" in response.data
    assert response.status_code == 302


def test_register_user_password_mismatch(test_client, init_database):

    test_client.get("/register")
    form = RegisterForm(email="testkljj50@example.com", pseudo="testuser12", password="Test123", password_confirmation="Test123!")

    response = test_client.post(
        "/register",
        data=form.data,
        
    )
    print(response.data)

    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data
    assert b"Password dont match !" in response.data




def test_duplicate_registration(test_client, init_database):

    form = RegisterForm(email="test5@example.com", pseudo="testuser", password="Test123!", password_confirmation="Test123!")

    test_client.post(
        "/register",
        data=dict(
            email="testalreadyexist@gmail.com",
            pseudo="test",
            password="FlaskIsGreat123!",
            password_confirmation="FlaskIsGreat123!",
        ), 
    )
    # response = test_client.post("/register", data=form.data)
    with test_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None


    # Try registering with the same email address
    response = test_client.post(
        "/register",
        data=dict(
            email="testalreadyexist@gmail.com",
            pseudo="test",
            password="FlaskIsGreat123!",
            password_confirmation="FlaskIsGreat123!",
        ),  
        follow_redirects=True,
    )

   
    assert b'email already exists' in response.data