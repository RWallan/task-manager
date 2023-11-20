from __future__ import annotations

from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TaskStatus(str, Enum):
    draft = "draft"
    todo = "todo"
    doing = "doing"
    done = "done"
    thrash = "thrash"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(index=True, nullable=False)

    tasks: Mapped[list[Task]] = relationship(
        back_populates="users", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[TaskStatus] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"))

    users: Mapped[User] = relationship(back_populates="tasks")
