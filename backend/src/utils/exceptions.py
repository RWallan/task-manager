from fastapi import HTTPException, status


class DuplicatedRegister(HTTPException):
    def __init__(self, column: str) -> None:
        detail = f"{column} já registrado."

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class CredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais.",
            headers={"WWW-Authenticate": "Bearer"},
        )
