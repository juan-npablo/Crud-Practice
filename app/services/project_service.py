from sqlalchemy.orm import Session
from db.models.project import Project
from db.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, user_id: int, project: ProjectCreate) -> Project:
    new_project = Project(
        name=project.name,
        description=project.description,
        user_id=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project_for_user(db: Session, user_id: int) -> list[Project]:
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project_by_id(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.project_id == project_id).first()

def update_project(db: Session, project: Project, project_update: ProjectUpdate) -> Project | None:
    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int) -> bool:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        return True
    return False