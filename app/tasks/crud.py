from sqlalchemy.orm import Session
from tasks.models import Task
from tasks.schemas import TaskCreate, TaskUpdate
from typing import Optional
from datetime import datetime

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int):
    task = get_task(db, task_id, user_id)
    if task:
        for key, value in task_update.dict().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    if task:
        db.delete(task)
        db.commit()
    return task

def search_tasks(db: Session, user_id: int, title: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    query = db.query(Task).filter(Task.user_id == user_id)
    if title:
        query = query.filter(Task.title.contains(title))
    if start_date and end_date:
        query = query.filter(Task.deadline.between(start_date, end_date))
    return query.all()
