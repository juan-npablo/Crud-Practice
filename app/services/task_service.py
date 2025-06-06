from sqlalchemy.orm import Session
from db.models.task import Task
from db.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, project_id: int, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_for_project(db: Session, project_id: int) -> list[Task]:
    return db.query(Task).filter(Task.project_id == project_id).all()

def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.task_id == task_id).first()

def update_task(db: Session, task: Task, task_update: TaskUpdate) -> Task | None:
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.state is not None:
        task.state = task_update.state
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False