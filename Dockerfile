FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false
ENV DATABASE_URL=sqlite:///backend/data/database.db
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

RUN pip3 install poetry

RUN poetry config installer.max-workers 10

COPY . .

RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "backend.src.app:app"]
