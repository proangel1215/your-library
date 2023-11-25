from app.forms import LoginForm


def test_login_route(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_fail_wrong_credentials(test_client, init_database):
    form = LoginForm(email="test@example.com", password="Test123")

    response = test_client.post(
        "/login",
        data=form.data,
    )

    print(response.data)

    assert response.status_code == 200
    assert b"Wrong credentials" in response.data


def test_login_success(test_client, init_database):
    test_client.get("/login")

    form = LoginForm(email="user1@gmail.com", password="User123!")

    response = test_client.post("/login", data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome user1 !" in response.data

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200

    assert b"Logout" not in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data


def test_login_already_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/login",
        data=dict(email="user2@gmail.com", password="User234!"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Already logged in!  Redirecting to home page..." in response.data

    assert b"Logout" in response.data

    assert b"Login" not in response.data
    assert b"Register" not in response.data
