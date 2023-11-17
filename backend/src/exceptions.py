from fastapi import HTTPException, status


class DuplicatedRegister(HTTPException):
    def __init__(self, column: str) -> None:
        detail = f"{column} já registrado."

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )
