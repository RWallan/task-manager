def test_api_must_be_online(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "online"}
