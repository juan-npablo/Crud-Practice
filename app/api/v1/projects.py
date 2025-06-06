from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.schemas.project import ProjectCreate, ProjectUpdate, ProjectUpdate, ProjectRead
from db.session import get_db
from services.project_service import (
    create_project,
    get_project_for_user,
    get_project_by_id,
    update_project,
    delete_project
)

from api.deps import get_current_user
from db.models.user import User
from db.models.project import Project

router = APIRouter()

@router.get("/", response_model=List[ProjectRead])
def read_projects(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> List[ProjectRead]:
    projects = get_project_for_user(db, current_user.user_id)
    return projects

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> ProjectRead:
    new_project = create_project(db, project, current_user.user_id)
    return new_project

@router.get("/{project_id}", response_model=ProjectRead)
def read_project(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> ProjectRead:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return project

@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, 
    project: ProjectUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> ProjectRead:
    updated_project = get_project_by_id(db, project_id, current_user.user_id)
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return updated_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> None:
    project = get_project_by_id(db, project_id, current_user.user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    delete_project(db, project_id)
    return None