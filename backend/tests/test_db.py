from backend.src.database.models import Task, User


def test_create_user(session):
    new_user = User(
        username="alice", password="secret", email="teste@test.com"
    )
    session.add(new_user)
    session.commit()

    user = session.query(User).where(User.username == "alice").first()

    assert user.username == "alice"


def test_create_task(session, user):
    task = Task(
        title="title", description="desc", state="draft", user_id=user.id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    user = session.query(User).where(User.id == user.id).first()

    assert task in user.tasks
