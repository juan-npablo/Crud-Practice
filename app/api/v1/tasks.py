from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.schemas.task import TaskCreate, TaskUpdate, TaskRead
from db.models.task import Task
from db.session import get_db
from services.task_service import (
    create_task,
    get_tasks_for_project,
    get_task_by_id,
    update_task,
    delete_task
)
from services.project_service import get_project_by_id
from api.deps import get_current_user
from db.models.user import User


router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Task] | None:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto"
        )
    return get_tasks_for_project(db, project_id)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_new_task(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskRead:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto"
        )
    return create_task(db, project_id, task)

@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskRead:
    project = get_project_by_id(db, task_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto"
        )
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    project_id: int,
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskRead:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto"
        )
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return update_task(db, task, task_update)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto"
        )
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    delete_task(db, task_id)
    return None