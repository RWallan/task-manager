from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.src.database.models import TaskStatus


class TaskBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    state: Optional[TaskStatus]


class TaskCreate(TaskBase):
    title: str
    state: TaskStatus


class TaskInDBBase(TaskBase):
    id: int
    title: str
    state: TaskStatus

    model_config = ConfigDict(from_attributes=True)


class Task(TaskInDBBase):
    pass

