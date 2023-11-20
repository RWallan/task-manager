from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.src import controllers, schemas
from backend.src.database.init_session import get_session
from backend.src.database.models import User
from backend.src.utils.exceptions import DuplicatedRegister
from backend.src.utils.security import get_current_user

router = APIRouter()


@router.post(
    "/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_email = controllers.user.read_by_email(db, email=user.email)
    if db_email:
        raise DuplicatedRegister("E-mail")

    db_username = controllers.user.read_by_username(db, username=user.username)
    if db_username:
        raise DuplicatedRegister("Username")

    created_user = controllers.user.create(db, obj_in=user)

    return created_user


@router.get(
    "/users/", status_code=status.HTTP_200_OK, response_model=schemas.UserList
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
):
    users = controllers.user.read_multiple(db, skip=skip, limit=limit)

    return schemas.UserList(users=users)


@router.put("/users/{id}", response_model=schemas.User)
def update_user(
    id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sem permissão."
        )

    try:
        updated_user = controllers.user.update(db, id=id, obj_in=user)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error
        )

    return updated_user


@router.delete("/users/{id}", response_model=schemas.Msg)
def delete_user(
    id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sem permissão."
        )

    try:
        _ = controllers.user.delete(db, id=id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error
        )

    return schemas.Msg(msg="Usuário deletado.")
