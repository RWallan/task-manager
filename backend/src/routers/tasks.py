from fastapi import APIRouter

from backend.src import controllers, schemas
from backend.src.utils.deps import CurrentUser, Session

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate, session: Session, current_user: CurrentUser
):
    task_created = controllers.task.create(
        session, obj_in=task, user_id=current_user.id
    )

    return task_created
