from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    project_id: Optional[int]
    name: str
    description: Optional[int] = None
    user_id: int
    created_at: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    pass
    class Config:
        orm_mode = True


