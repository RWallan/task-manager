from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.src.controllers._base import CRUDBase
from backend.src.database.models import User
from backend.src.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def read_by_email(self, db: Session, *, email: EmailStr) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def read_by_username(
        self, db: Session, *, username: str
    ) -> Optional[User]:
        return (
            db.query(self.model)
            .filter(self.model.username == username)
            .first()
        )


user = CRUDUser(User)
