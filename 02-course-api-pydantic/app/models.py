from typing import Optional
from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    price: float = Field(gt=0)
    duration: str = Field(min_length=2)
    instructor: str = Field(min_length=2)
    category: str = Field(min_length=2)
    rating: float = Field(ge=0.0, le=5.0)
    active: bool = True

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, min_length=10, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)
    duration: Optional[str] = Field(default=None, min_length=2)
    instructor: Optional[str] = Field(default=None, min_length=2)
    category: Optional[str] = Field(default=None, min_length=2)
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    active: Optional[bool] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    duration: str
    instructor: str
    category: str
    rating: float
    active: bool