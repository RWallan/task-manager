from backend.src.utils.security import Hasher, JWTToken


def test_jwt():
    data = {"test": "test"}
    token = JWTToken.encode(data)
    decoded = JWTToken.decode(token)

    assert decoded["test"] == "test"
    assert decoded["exp"]


def test_hash_with_correct_password():
    pwd = "12345"

    hashed_pwd = Hasher.get_password_hash(pwd)

    assert Hasher.verify_password(pwd, hashed_pwd)


def test_hash_with_incorrect_password():
    pwd = "12345"

    hashed_pwd = Hasher.get_password_hash(pwd)

    assert not Hasher.verify_password("1234", hashed_pwd)
