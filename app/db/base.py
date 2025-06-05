from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.db.models.user import User  # noqa
from app.db.models.project import Project  # noqa
from app.db.models.task import Task  # noqa
