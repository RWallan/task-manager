from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.src.controllers._base import CRUDBase
from backend.src.database.models import User
from backend.src.schemas import UserCreate, UserUpdate
from backend.src.utils.security import Hasher


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

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_obj_in = UserCreate(
            username=obj_in.username,
            email=obj_in.email,
            password=Hasher.get_password_hash(obj_in.password),
        )

        return super().create(db, obj_in=hashed_obj_in)

    def update(self, db: Session, *, id: int, obj_in: UserUpdate) -> User:
        if obj_in.password:
            obj_in.password = Hasher.get_password_hash(obj_in.password)

        return super().update(db, id=id, obj_in=obj_in)


user = CRUDUser(User)
