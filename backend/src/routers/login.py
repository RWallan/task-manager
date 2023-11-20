from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.src import controllers, schemas
from backend.src.database.init_session import get_session
from backend.src.utils.security import JWTToken

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = controllers.user.authenticate(
        session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha incorreto.",
        )

    access_token = JWTToken.encode(data={"sub": user.id})

    return schemas.Token(access_token=access_token, token_type="bearer")
