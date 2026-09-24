from pydantic import BaseModel, Field, ConfigDict

class ProjectCreate(BaseModel):
    title: str
    description: str | None = None

class ProjectResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str | None = None

    model_config = ConfigDict(
        populate_by_name=True
    )

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    project_id: str
    assignee_name: str | None = None

class TaskStatusUpdate(BaseModel):
    status: str

class TaskAssignUpdate(BaseModel):
    assignee_name: str

class TaskResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str | None = None
    status: str = "TODO"
    assignee_name: str | None = None
    project_id: str

    model_config = ConfigDict(
        populate_by_name=True
    )