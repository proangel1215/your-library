from app import create_app


def test_register_route(test_client):
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data
