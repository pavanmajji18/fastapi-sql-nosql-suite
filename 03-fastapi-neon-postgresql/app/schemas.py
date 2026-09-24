from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Student Models
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    city: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    city: Optional[str] = None

# Course Models
class CourseCreate(BaseModel):
    title: str
    instructor: Optional[str] = None
    price: float
    duration_hours: Optional[int] = None

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    instructor: Optional[str] = None
    price: Optional[float] = None
    duration_hours: Optional[int] = None

# Enrollment Models
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    status: Optional[str] = "active"

class EnrollmentUpdate(BaseModel):
    status: str