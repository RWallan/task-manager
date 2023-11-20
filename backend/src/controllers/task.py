from sqlalchemy.orm import Session

from backend.src.controllers._base import CRUDBase
from backend.src.database.models import Task
from backend.src.schemas import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create(self, db: Session, *, obj_in: TaskCreate, user_id: int) -> Task:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data, user_id=user_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


task = CRUDTask(Task)
