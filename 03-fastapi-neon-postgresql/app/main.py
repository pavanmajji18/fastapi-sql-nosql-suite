from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.schemas import (
    StudentCreate, StudentUpdate,
    CourseCreate, CourseUpdate,
    EnrollmentCreate, EnrollmentUpdate
)

app = FastAPI(title="Student & Course Management API (Neon DB)")

# ==================== STUDENTS ====================

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    try:
        query = text("""
            INSERT INTO student (name, email, age, city)
            VALUES (:name, :email, :age, :city)
            RETURNING id, name, email, age, city, created_at
        """)
        result = db.execute(query, payload.model_dump()).mappings().first()
        db.commit()
        return {"status": "success", "data": dict(result)}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM student ORDER BY id ASC")).mappings().all()
    return {"status": "success", "data": [dict(r) for r in result]}

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM student WHERE id = :id"), {"id": student_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"status": "success", "data": dict(result)}

@app.patch("/students/{student_id}")
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    fields_to_update = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields_to_update:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    set_clause = ", ".join([f"{k} = :{k}" for k in fields_to_update.keys()])
    fields_to_update["id"] = student_id
    
    try:
        query = text(f"UPDATE student SET {set_clause} WHERE id = :id RETURNING *")
        result = db.execute(query, fields_to_update).mappings().first()
        if not result:
            db.rollback()
            raise HTTPException(status_code=404, detail="Student not found")
        db.commit()
        return {"status": "success", "data": dict(result)}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM student WHERE id = :id RETURNING id")
    result = db.execute(query, {"id": student_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db.commit()
    return {"status": "success", "message": f"Student {student_id} and related enrollments deleted successfully"}

# ==================== COURSES ====================

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    try:
        query = text("""
            INSERT INTO courses (title, instructor, price, duration_hours)
            VALUES (:title, :instructor, :price, :duration_hours)
            RETURNING id, title, instructor, price, duration_hours, created_at
        """)
        result = db.execute(query, payload.model_dump()).mappings().first()
        db.commit()
        return {"status": "success", "data": dict(result)}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/courses")
def get_all_courses(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM courses ORDER BY id ASC")).mappings().all()
    return {"status": "success", "data": [dict(r) for r in result]}

@app.patch("/courses/{course_id}")
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    fields_to_update = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields_to_update:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    set_clause = ", ".join([f"{k} = :{k}" for k in fields_to_update.keys()])
    fields_to_update["id"] = course_id

    try:
        query = text(f"UPDATE courses SET {set_clause} WHERE id = :id RETURNING *")
        result = db.execute(query, fields_to_update).mappings().first()
        if not result:
            db.rollback()
            raise HTTPException(status_code=404, detail="Course not found")
        db.commit()
        return {"status": "success", "data": dict(result)}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM courses WHERE id = :id RETURNING id")
    result = db.execute(query, {"id": course_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Course not found")
    db.commit()
    return {"status": "success", "message": f"Course {course_id} deleted successfully"}

# ==================== ENROLLMENTS ====================

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def enroll_student(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        query = text("""
            INSERT INTO enrollment (student_id, course_id, status)
            VALUES (:student_id, :course_id, :status)
            RETURNING id, student_id, course_id, status, enrolled_at
        """)
        result = db.execute(query, payload.model_dump()).mappings().first()
        db.commit()
        return {"status": "success", "data": dict(result)}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/enrollments")
def get_enrollments(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            e.id AS enrollment_id,
            e.status,
            e.enrolled_at,
            s.id AS student_id,
            s.name AS student_name,
            s.email AS student_email,
            c.id AS course_id,
            c.title AS course_title,
            c.price AS course_price
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        JOIN courses c ON e.course_id = c.id
        ORDER BY e.enrolled_at DESC
    """)
    result = db.execute(query).mappings().all()
    return {"status": "success", "data": [dict(r) for r in result]}

@app.patch("/enrollments/{enrollment_id}")
def update_enrollment_status(enrollment_id: int, payload: EnrollmentUpdate, db: Session = Depends(get_db)):
    try:
        query = text("""
            UPDATE enrollment 
            SET status = :status 
            WHERE id = :id 
            RETURNING id, student_id, course_id, status, enrolled_at
        """)
        result = db.execute(query, {"status": payload.status, "id": enrollment_id}).mappings().first()
        if not result:
            db.rollback()
            raise HTTPException(status_code=404, detail="Enrollment record not found")
        db.commit()
        return {"status": "success", "data": dict(result)}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM enrollment WHERE id = :id RETURNING id")
    result = db.execute(query, {"id": enrollment_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Enrollment record not found")
    db.commit()
    return {"status": "success", "message": f"Enrollment {enrollment_id} deleted successfully"}

# ==================== ANALYTICS ====================

@app.get("/courses/revenue")
def get_course_revenue(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            c.id AS course_id,
            c.title,
            c.price,
            COUNT(e.id) AS total_students,
            (c.price * COUNT(e.id)) AS total_revenue
        FROM courses c
        JOIN enrollment e ON c.id = e.course_id
        GROUP BY c.id, c.title, c.price
        ORDER BY total_revenue DESC
    """)
    result = db.execute(query).mappings().all()
    return {"status": "success", "data": [dict(r) for r in result]}