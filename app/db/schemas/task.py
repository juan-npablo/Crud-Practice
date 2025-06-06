from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    state: str = "todo"
    

class TaskCreate(TaskBase):
    task_id: Optional[int] = None
    #project_id: int
    created_at: Optional[datetime] = None
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None

class TaskRead(TaskBase):
    pass

    class Config:
        orm_mode = True
