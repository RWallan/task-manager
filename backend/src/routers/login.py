from fastapi import APIRouter, HTTPException, status

from backend.src import controllers, schemas
from backend.src.utils.deps import OAuth2Form, Session
from backend.src.utils.security import JWTToken

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2Form,
    session: Session,
):
    user = controllers.user.authenticate(
        session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha incorreto.",
        )

    access_token = JWTToken.encode(data={"sub": str(user.id)})

    return schemas.Token(access_token=access_token, token_type="bearer")
