from backend.src import controllers
from backend.src.database.models import Task
from backend.src.schemas.task import TaskCreate


def test_create_task(session, user):
    obj_in = TaskCreate(
        title="title",
        description="desc",
        state="draft",
    )

    obj_out = controllers.task.create(session, obj_in=obj_in, user_id=user.id)

    assert obj_out.title == obj_in.title
    assert obj_out.user_id == user.id

    assert session.query(Task).filter(Task.user_id == user.id)
