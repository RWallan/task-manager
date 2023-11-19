from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from backend.src.utils.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTToken:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    SECRET_KEY: str = settings.SECRET_KEY
    ALGORITHM: str = settings.ALGORITHM

    @classmethod
    def encode(cls, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def decode(cls, token: str) -> dict[str, Any]:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
