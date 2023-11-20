def test_login_route(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert token["token_type"] == "bearer"
