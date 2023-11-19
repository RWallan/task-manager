from backend.src.utils.security import JWTToken


def test_jwt():
    data = {"test": "test"}
    token = JWTToken.encode(data)
    decoded = JWTToken.decode(token)

    assert decoded["test"] == "test"
    assert decoded["exp"]
