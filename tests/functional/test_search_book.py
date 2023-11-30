def test_search_book_page(test_client, init_database, log_in_default_user):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Search book" in response.data


def test_search_book_post(test_client, init_database, log_in_default_user):
    response = test_client.post("/", data=dict(search="YourSearchTerm"))
    assert response.status_code == 200
