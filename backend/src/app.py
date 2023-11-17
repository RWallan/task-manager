from fastapi import FastAPI

from backend.src.routers import user_router

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "online"}


app.include_router(user_router)
