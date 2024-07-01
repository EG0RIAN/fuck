from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from auth.auth import get_current_user
from tasks.schemas import TaskCreate, TaskUpdate, Task
from tasks.crud import create_task, get_task, update_task, delete_task, search_tasks

router = APIRouter()

@router.post("/create", response_model=Task)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_task(db, task, current_user.tg_id)

@router.put("/update/{task_id}", response_model=Task)
def update_task_endpoint(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_task(db, task_id, task, current_user.tg_id)

@router.delete("/delete/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_task(db, task_id, current_user.tg_id)
    return {"detail": "Task deleted"}

@router.get("/get/{task_id}", response_model=Task)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = get_task(db, task_id, current_user.tg_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/search", response_model=List[Task])
def search_tasks_endpoint(title: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return search_tasks(db, current_user.tg_id, title, start_date, end_date)
