from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    task_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    state: str = "todo"
    project_id: int
    created_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None

class TaskRead(TaskBase):
    pass

    class Config:
        orm_mode = True
