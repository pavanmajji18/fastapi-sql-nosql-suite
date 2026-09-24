from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from bson import ObjectId
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from app.database import get_db
from app.schemas import (
    ProjectCreate, ProjectResponse, TaskCreate, 
    TaskResponse, TaskStatusUpdate, TaskAssignUpdate
)

app = FastAPI(title="Task Management - MongoDB")

@app.exception_handler(ServerSelectionTimeoutError)
async def mongo_timeout_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Could not connect to MongoDB Atlas (ServerSelectionTimeoutError / SSL Handshake Failed).",
            "possible_causes": [
                "Your current IP address is not whitelisted in MongoDB Atlas Network Access.",
                "The MongoDB Atlas cluster is paused or unreachable."
            ],
            "solution": "Go to MongoDB Atlas -> Network Access -> Add Current IP Address (or 0.0.0.0/0)."
        }
    )

@app.exception_handler(PyMongoError)
async def mongo_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Database error: {str(exc)}"}
    )

def fix_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db = Depends(get_db)):
    doc = payload.model_dump()
    result = await db["projects"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db = Depends(get_db)):
    if not ObjectId.is_valid(payload.project_id):
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    
    project = await db["projects"].find_one({"_id": ObjectId(payload.project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    doc = payload.model_dump()
    doc["status"] = "TODO"
    result = await db["tasks"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

@app.patch("/tasks/{task_id}/assign", response_model=TaskResponse)
async def assign_task(task_id: str, payload: TaskAssignUpdate, db = Depends(get_db)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task_id")
    
    updated = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {"assignee_name": payload.assignee_name}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return fix_id(updated)

@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_status(task_id: str, payload: TaskStatusUpdate, db = Depends(get_db)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task_id")
    
    updated = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": payload.status}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return fix_id(updated)

@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    project_id: str | None = None,
    status: str | None = None,
    db = Depends(get_db)
):
    query = {}
    if project_id:
        query["project_id"] = project_id
    if status:
        query["status"] = status
        
    cursor = db["tasks"].find(query)
    tasks = await cursor.to_list(length=100)
    return [fix_id(t) for t in tasks]

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db = Depends(get_db)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task_id")
        
    result = await db["tasks"].delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")