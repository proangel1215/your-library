from app.models.User import User
from app import create_app, db
import pytest


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("config.TestingConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

    user1 = User(
        email="user1@gmail.com", username="user1", password_plaintext="User123!"
    )
    user2 = User(
        email="user2@gmail.com", username="user2", password_plaintext="User234!"
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield

    db.drop_all()
