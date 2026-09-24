import time
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query, Request, status
from app.models import CourseCreate, CourseUpdate, CourseResponse
from app.security import verify_api_key
import app.database as db

app = FastAPI(
    title="Course Management API",
    description="FastAPI + Pydantic backend implementation",
    version="1.0.0"
)

def rate_limiter(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    timestamps = [t for t in db.request_history.get(client_ip, []) if current_time - t < 60]
    
    if len(timestamps) >= 10:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
    timestamps.append(current_time)
    db.request_history[client_ip] = timestamps

@app.get("/")
def root():
    return {"message": "Course Management API is running"}

@app.post(
    "/courses", 
    response_model=CourseResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
def create_course(course: CourseCreate):
    course_data = course.model_dump()
    course_data["id"] = db.course_id_counter
    db.courses_db[db.course_id_counter] = course_data
    db.course_id_counter += 1
    return course_data

@app.get("/courses", response_model=list[CourseResponse], dependencies=[Depends(rate_limiter)])
def get_courses(
    category: Optional[str] = Query(default=None),
    min_price: Optional[float] = Query(default=None, gt=0),
    max_price: Optional[float] = Query(default=None, gt=0),
    active: Optional[bool] = Query(default=None)
):
    results = list(db.courses_db.values())
    if category is not None:
        results = [c for c in results if c["category"].lower() == category.lower()]
    if min_price is not None:
        results = [c for c in results if c["price"] >= min_price]
    if max_price is not None:
        results = [c for c in results if c["price"] <= max_price]
    if active is not None:
        results = [c for c in results if c["active"] == active]
    return results

@app.get("/courses/{course_id}", response_model=CourseResponse, dependencies=[Depends(rate_limiter)])
def get_course_by_id(course_id: int):
    if course_id not in db.courses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return db.courses_db[course_id]

@app.put(
    "/courses/{course_id}", 
    response_model=CourseResponse,
    dependencies=[Depends(verify_api_key)]
)
def update_course(course_id: int, course: CourseCreate):
    if course_id not in db.courses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    updated_data = course.model_dump()
    updated_data["id"] = course_id
    db.courses_db[course_id] = updated_data
    return updated_data

@app.patch(
    "/courses/{course_id}", 
    response_model=CourseResponse,
    dependencies=[Depends(verify_api_key)]
)
def patch_course(course_id: int, course: CourseUpdate):
    if course_id not in db.courses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    update_data = course.model_dump(exclude_unset=True)
    db.courses_db[course_id].update(update_data)
    return db.courses_db[course_id]

@app.delete(
    "/courses/{course_id}", 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_api_key)]
)
def delete_course(course_id: int):
    if course_id not in db.courses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    del db.courses_db[course_id]
    return {"message": f"Course {course_id} deleted successfully"}