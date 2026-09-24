from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models import TaskStatus

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    project_id: UUID
    assignee_name: str | None = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class TaskAssignUpdate(BaseModel):
    assignee_name: str

class TaskResponse(TaskBase):
    id: UUID
    status: TaskStatus
    assignee_name: str | None = None
    project_id: UUID
    model_config = ConfigDict(from_attributes=True)