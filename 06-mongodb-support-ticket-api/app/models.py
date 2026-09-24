from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, BeforeValidator, EmailStr, Field

# Custom helper to map MongoDB ObjectId to string
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if v is not None else None)]


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Customer(BaseModel):
    name: str = Field(..., examples=["Pavan Kumar"])
    email: EmailStr = Field(..., examples=["pavan.kumar@example.com"])
    phone: Optional[str] = Field(None, examples=["+91-9876543210"])


class Comment(BaseModel):
    author: str = Field(..., examples=["Santosh Kumar"])
    message: str = Field(..., examples=["Investigating the backend gateway latency."])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CommentCreate(BaseModel):
    author: str = Field(..., examples=["Rakesh Kumar"])
    message: str = Field(..., examples=["Assigned to infrastructure operations team."])


class TicketCreate(BaseModel):
    customer: Customer
    title: str = Field(..., min_length=5, max_length=200, examples=["Payment Gateway Timeout on Checkout"])
    description: str = Field(..., min_length=10, examples=["Customers experiencing timeout errors during UPI checkout."])
    category: str = Field(..., examples=["Billing"])
    priority: PriorityEnum = PriorityEnum.MEDIUM
    tags: List[str] = Field(default_factory=list, examples=[["payment", "upi", "high-priority"]])


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    tags: Optional[List[str]] = None


class StatusUpdate(BaseModel):
    status: StatusEnum


class TicketResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    customer: Customer
    title: str
    description: str
    category: str
    priority: PriorityEnum
    status: StatusEnum
    comments: List[Comment] = []
    tags: List[str] = []
    created_date: datetime
    updated_date: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: lambda dt: dt.isoformat()},
    }