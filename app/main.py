from fastapi import FastAPI
from database.database import engine, Base
from auth.router import router as auth_router
from tasks.router import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
