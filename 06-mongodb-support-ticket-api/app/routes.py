from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.models import (
    Comment,
    CommentCreate,
    PriorityEnum,
    StatusEnum,
    StatusUpdate,
    TicketCreate,
    TicketResponse,
    TicketUpdate,
)

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])


def parse_object_id(ticket_id: str) -> ObjectId:
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ticket ID format: '{ticket_id}'",
        )
    return ObjectId(ticket_id)


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: TicketCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    now = datetime.now(timezone.utc)
    ticket_doc = payload.model_dump()
    ticket_doc.update({
        "status": StatusEnum.OPEN.value,
        "comments": [],
        "created_date": now,
        "updated_date": now,
    })

    result = await db["tickets"].insert_one(ticket_doc)
    created_ticket = await db["tickets"].find_one({"_id": result.inserted_id})
    return created_ticket


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    priority: Optional[PriorityEnum] = None,
    status: Optional[StatusEnum] = None,
    category: Optional[str] = None,
    search: Optional[str] = Query(None, description="Keyword search in title, description, or tags"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    query_filter = {}

    if priority:
        query_filter["priority"] = priority.value
    if status:
        query_filter["status"] = status.value
    if category:
        query_filter["category"] = category
    if search:
        query_filter["$text"] = {"$search": search}

    cursor = db["tickets"].find(query_filter).sort("created_date", -1).skip(skip).limit(limit)
    tickets = await cursor.to_list(length=limit)
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    obj_id = parse_object_id(ticket_id)
    ticket = await db["tickets"].find_one({"_id": obj_id})
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    payload: TicketUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    obj_id = parse_object_id(ticket_id)
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    update_data["updated_date"] = datetime.now(timezone.utc)

    result = await db["tickets"].find_one_and_update(
        {"_id": obj_id},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return result


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
async def change_ticket_status(
    ticket_id: str,
    payload: StatusUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    obj_id = parse_object_id(ticket_id)
    result = await db["tickets"].find_one_and_update(
        {"_id": obj_id},
        {
            "$set": {
                "status": payload.status.value,
                "updated_date": datetime.now(timezone.utc),
            }
        },
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return result


@router.post("/{ticket_id}/comments", response_model=TicketResponse)
async def add_comment_to_ticket(
    ticket_id: str,
    payload: CommentCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    obj_id = parse_object_id(ticket_id)
    comment = Comment(author=payload.author, message=payload.message)
    now = datetime.now(timezone.utc)

    result = await db["tickets"].find_one_and_update(
        {"_id": obj_id},
        {
            "$push": {"comments": comment.model_dump()},
            "$set": {"updated_date": now},
        },
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return result


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    obj_id = parse_object_id(ticket_id)
    result = await db["tickets"].delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return None