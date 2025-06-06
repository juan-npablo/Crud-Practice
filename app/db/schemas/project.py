from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    

class ProjectCreate(ProjectBase):
    project_id: Optional[int]
    user_id: int
    created_at: Optional[datetime] = None


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    pass
    class Config:
        orm_mode = True


