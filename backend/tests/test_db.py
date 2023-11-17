from backend.src.database.models import User


def test_create_user(session):
    new_user = User(
        username="alice", password="secret", email="teste@test.com"
    )
    session.add(new_user)
    session.commit()

    user = session.query(User).where(User.username == "alice").first()

    assert user.username == "alice"
