from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Project, Task, TaskStatus
from app.schemas import ProjectCreate, TaskCreate, TaskStatusUpdate, TaskAssignUpdate

async def create_project(db: AsyncSession, payload: ProjectCreate) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

async def get_project(db: AsyncSession, project_id: UUID) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()

async def create_task(db: AsyncSession, payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, task_id: UUID) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def update_task_assignee(db: AsyncSession, task: Task, payload: TaskAssignUpdate) -> Task:
    task.assignee_name = payload.assignee_name
    await db.commit()
    await db.refresh(task)
    return task

async def update_task_status(db: AsyncSession, task: Task, payload: TaskStatusUpdate) -> Task:
    task.status = payload.status
    await db.commit()
    await db.refresh(task)
    return task

async def list_tasks(
    db: AsyncSession,
    project_id: UUID | None = None,
    status: TaskStatus | None = None
) -> list[Task]:
    query = select(Task)
    if project_id:
        query = query.where(Task.project_id == project_id)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return list(result.scalars().all())

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()