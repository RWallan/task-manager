import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.src.app import app
from backend.src.database.init_session import get_session
from backend.src.database.models import Base, User
from backend.src.utils.security import Hasher


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(
        username="Teste",
        email="teste@teste.com",
        password=Hasher.get_password_hash("teste"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = "teste"

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    return response.json()["access_token"]
