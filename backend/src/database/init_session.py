from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.src.utils.settings import Settings

engine = create_engine(url=Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
