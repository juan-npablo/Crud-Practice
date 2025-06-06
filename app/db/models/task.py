from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base_class import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String(500), nullable=True)
    state = Column(String(50), default="todo", nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    project = relationship("Project", back_populates="tasks")