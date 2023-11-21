from typing import Optional

from sqlalchemy.orm import Session

from backend.src.controllers._base import CRUDBase
from backend.src.database.models import Task
from backend.src.schemas import TaskCreate, TaskQuery, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create(self, db: Session, *, obj_in: TaskCreate, user_id: int) -> Task:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data, user_id=user_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def read_by_user_id(self, db: Session, *, user_id: int) -> Optional[Task]:
        return db.query(self.model).filter(self.model.user_id == user_id)

    def query_task(
        self,
        db: Session,
        *,
        user_id: int,
        task_query: TaskQuery,
        offset: int = 0,
        limit: int = 100,
    ) -> Optional[list[Task]]:
        query = self.read_by_user_id(db, user_id=user_id)

        if task_query.title:
            query = query.filter(self.model.title.contains(task_query.title))

        if task_query.description:
            query = query.filter(
                self.model.description.contains(task_query.description)
            )

        if task_query.state:
            query = query.filter(self.model.state == task_query.state)

        tasks = query.offset(offset).limit(limit).all()

        return tasks


task = CRUDTask(Task)
