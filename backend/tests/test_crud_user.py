from backend.src import controllers
from backend.src.database.models import User
from backend.src.schemas import UserCreate, UserUpdate


def test_create_user_must_return_user(session):
    obj_in = UserCreate(
        username="teste", email="teste@teste.com", password="teste"
    )

    obj_out = controllers.user.create(session, obj_in=obj_in)

    assert obj_out.username == obj_in.username
    assert session.query(User).filter(User.username == obj_in.username).first()


def test_read_user_by_id(session, user):
    obj_out = controllers.user.read_by_id(session, id=user.id)

    assert obj_out.id == user.id


def test_read_user_by_email(session, user):
    obj_out = controllers.user.read_by_email(session, email=user.email)

    assert obj_out.email == user.email


def test_read_multiple_users(session, user):
    obj_out = controllers.user.read_multiple(session)

    assert obj_out == [user]


def test_update_all(session, user):
    obj_in = UserUpdate(username="abc", email="abc@abc.com", password="abc")

    obj_out = controllers.user.update(session, id=user.id, obj_in=obj_in)

    assert obj_out.username == obj_in.username
    assert obj_out.email == obj_in.email
    assert obj_out.password == obj_in.password

    assert session.query(User).filter(User.username == obj_in.username).first()
    assert session.query(User).filter(User.email == obj_in.email).first()
    assert session.query(User).filter(User.password == obj_in.password).first()


def test_partial_update(session, user):
    obj_in = UserUpdate(username="abc", password="abc")

    obj_out = controllers.user.update(session, id=user.id, obj_in=obj_in)

    assert obj_out.username == obj_in.username
    assert obj_out.email == user.email
    assert obj_out.password == obj_in.password

    assert session.query(User).filter(User.username == obj_in.username).first()
    assert session.query(User).filter(User.email == user.email).first()
    assert session.query(User).filter(User.password == obj_in.password).first()


def test_delete_user(session, user):
    obj_out = controllers.user.delete(session, id=user.id)

    assert obj_out == user
    assert not session.query(User).filter(User.id == user.id).first()
