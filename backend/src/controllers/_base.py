from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.src.database.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def read_by_id(self, db: Session, *, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def read_multiple(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self, db: Session, *, id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.read_by_id(db, id=id)

        if not db_obj:
            raise Exception("Usuário não encontrado.")

        for field in obj_data:
            if obj_data[field]:
                setattr(db_obj, field, obj_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        db_obj = self.read_by_id(db, id=id)

        if not db_obj:
            raise Exception("Usuário não encontrado.")

        db.delete(db_obj)
        db.commit()

        return db_obj
