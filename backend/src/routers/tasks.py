from fastapi import APIRouter, HTTPException, Query, status

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


@router.get("/", response_model=schemas.TaskList)
def read_tasks(
    session: Session,
    current_user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: str = Query(0),
    limit: str = Query(100),
):
    task_query = schemas.TaskQuery(
        title=title, description=description, state=state
    )

    tasks = controllers.task.query_task(
        session,
        user_id=current_user.id,
        task_query=task_query,
        offset=offset,
        limit=limit,
    )

    return schemas.TaskList(tasks=tasks)


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    session: Session,
    current_user: CurrentUser,
):
    to_update_task = controllers.task.read_by_id(session, id=task_id)

    if not to_update_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada"
        )

    if to_update_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem permissão."
        )

    updated_task = controllers.task.update(session, id=task_id, obj_in=task)

    return updated_task
