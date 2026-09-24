from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas import ProjectCreate, TaskCreate, TaskStatusUpdate, TaskAssignUpdate

def serialize_doc(doc: dict | None) -> dict | None:
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

async def create_project(db: AsyncIOMotorDatabase, payload: ProjectCreate) -> dict:
    doc = payload.model_dump()
    result = await db["projects"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

async def get_project_by_id(db: AsyncIOMotorDatabase, project_id: str) -> dict | None:
    if not ObjectId.is_valid(project_id):
        return None
    doc = await db["projects"].find_one({"_id": ObjectId(project_id)})
    return serialize_doc(doc)

async def create_task(db: AsyncIOMotorDatabase, payload: TaskCreate) -> dict:
    doc = payload.model_dump()
    doc["status"] = "TODO"
    result = await db["tasks"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

async def update_task_assignee(db: AsyncIOMotorDatabase, task_id: str, payload: TaskAssignUpdate) -> dict | None:
    if not ObjectId.is_valid(task_id):
        return None
    doc = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {"assignee_name": payload.assignee_name}},
        return_document=True
    )
    return serialize_doc(doc)

async def update_task_status(db: AsyncIOMotorDatabase, task_id: str, payload: TaskStatusUpdate) -> dict | None:
    if not ObjectId.is_valid(task_id):
        return None
    doc = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": payload.status}},
        return_document=True
    )
    return serialize_doc(doc)

async def list_tasks(
    db: AsyncIOMotorDatabase,
    project_id: str | None = None,
    status: str | None = None,
    limit: int = 100
) -> list[dict]:
    query = {}
    if project_id:
        query["project_id"] = project_id
    if status:
        query["status"] = status

    cursor = db["tasks"].find(query)
    raw_tasks = await cursor.to_list(length=limit)
    return [serialize_doc(t) for t in raw_tasks if t is not None]

async def delete_task(db: AsyncIOMotorDatabase, task_id: str) -> bool:
    if not ObjectId.is_valid(task_id):
        return False
    result = await db["tasks"].delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0