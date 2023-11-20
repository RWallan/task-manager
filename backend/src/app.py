from fastapi import FastAPI

from backend.src import routers

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "online"}


app.include_router(routers.user_router)
app.include_router(routers.login_router)
app.include_router(routers.task_router)
