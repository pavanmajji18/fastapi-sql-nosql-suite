from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from contextlib import asynccontextmanager

from app.database import Base, engine, get_db
from app.models import Project, Task, TaskStatus
from app.schemas import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse, TaskStatusUpdate, TaskAssignUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Task Management - PostgreSQL", lifespan=lifespan)

@app.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == payload.project_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")
    
    task = Task(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@app.patch("/tasks/{task_id}/assign", response_model=TaskResponse)
async def assign_task(task_id: UUID, payload: TaskAssignUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assignee_name = payload.assignee_name
    await db.commit()
    await db.refresh(task)
    return task

@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_status(task_id: UUID, payload: TaskStatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = payload.status
    await db.commit()
    await db.refresh(task)
    return task

@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    project_id: UUID | None = None,
    status: TaskStatus | None = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Task)
    if project_id:
        query = query.where(Task.project_id == project_id)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()