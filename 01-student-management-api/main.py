from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="Student Management REST API",
    description="A CRUD REST API demonstrating HTTP verbs, status codes, and Pydantic validation.",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=50, example="Pavan Majji")
    email: EmailStr = Field(example="Pavan.Majji@example.com")
    age: int = Field(gt=4, lt=100, example=20)
    major: str = Field(min_length=2, max_length=50, example="Computer Science")
    gpa: float = Field(ge=0.0, le=4.0, example=3.75)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, gt=4, lt=100)
    major: Optional[str] = Field(default=None, min_length=2, max_length=50)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


class StudentResponse(StudentBase):
    id: int


# ---------------------------------------------------------------------------
# In-Memory Database & State
# ---------------------------------------------------------------------------

students_db: Dict[int, dict] = {}
id_counter = 1


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
def create_student(student: StudentCreate):
    global id_counter

    # Check for unique email constraint
    for existing in students_db.values():
        if existing["email"] == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with email '{student.email}' already exists."
            )

    student_id = id_counter
    id_counter += 1

    student_record = student.model_dump()
    student_record["id"] = student_id
    students_db[student_id] = student_record

    return student_record


@app.get(
    "/students",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    tags=["Students"]
)
def list_students(
    major: Optional[str] = Query(None, description="Filter by major (case-insensitive)"),
    min_gpa: Optional[float] = Query(None, ge=0.0, le=4.0, description="Filter by minimum GPA")
):
    results = list(students_db.values())

    if major:
        results = [s for s in results if s["major"].lower() == major.lower()]

    if min_gpa is not None:
        results = [s for s in results if s["gpa"] >= min_gpa]

    return results


@app.get(
    "/students/{id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"]
)
def get_student(id: int):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )
    return students_db[id]


@app.put(
    "/students/{id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"]
)
def replace_student(id: int, student: StudentCreate):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )

    # Check email conflict with other records
    for s_id, s in students_db.items():
        if s_id != id and s["email"] == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{student.email}' is already in use by another student."
            )

    # Full replacement
    updated_record = student.model_dump()
    updated_record["id"] = id
    students_db[id] = updated_record

    return updated_record


@app.patch(
    "/students/{id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"]
)
def update_student(id: int, student: StudentUpdate):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )

    # Extract only explicitly passed fields per class notes
    update_data = student.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update."
        )

    # Check email duplicate if updating email
    if "email" in update_data:
        for s_id, s in students_db.items():
            if s_id != id and s["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{update_data['email']}' is already in use."
                )

    students_db[id].update(update_data)
    return students_db[id]


@app.delete(
    "/students/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"]
)
def delete_student(id: int):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )
    del students_db[id]
    return None