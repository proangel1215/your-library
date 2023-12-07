import pytest
from app.models.User import User


def test_new_user():
    user = User(email="test1@gmail.com", username="test", password_plaintext="Test123!")
    assert user.email == "test1@gmail.com"
    assert user.username == "test"
    assert user.is_password_correct("Test123!") == True


def test_raise_exception_for_username():
    with pytest.raises(AssertionError):
        user = User(email="test@gmail.com", username="", password_plaintext="Test123!")
    with pytest.raises(AssertionError):
        user = User(email="test@gmail.com", username="d", password_plaintext="Test123!")

    username = "t" * 51
    with pytest.raises(AssertionError):
        user = User(
            email="test@gmail.com", username=username, password_plaintext="Test123!"
        )


def test_raise_exception_for_email():
    with pytest.raises(AssertionError):
        user = User(email="", username="test", password_plaintext="Test123!")
    with pytest.raises(AssertionError):
        user = User(
            email="testgmail.com", username="test", password_plaintext="Test123!"
        )

    email = "@t" * 51

    with pytest.raises(AssertionError):
        user = User(email=email, username="test", password_plaintext="Test123!")
