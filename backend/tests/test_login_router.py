from freezegun import freeze_time


def test_login_route(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_token_expired_after_time(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/login",
            data={"username": user.email, "password": user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
                "password": "wrong",
            },
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Não foi possível validar as credenciais."
        }


def test_token_inexistent_user(client):
    response = client.post(
        "/auth/login",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail ou senha incorreto."}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "wrong_password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail ou senha incorreto."}
