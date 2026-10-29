from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database_skr import models  # noqa: F401
from database_skr.database import Base, SessionLocal, engine
from database_skr.shemas import StudentCreate, StudentResponse
from database_skr.student import Student


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
title="Система обліку студентів",
lifespan=lifespan,
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
     yield db
    finally:
      db.close()

@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Система обліку студентів працює"}

@app.get("/students", response_model=list[StudentResponse])
def get_students(
db: Session = Depends(get_db),
) -> list[Student]:
    return list(db.scalars(select(Student)).all())
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
) -> Student:
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Студента не знайдено")

    return student
@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(
student_data: StudentCreate,
db: Session = Depends(get_db),
) -> Student:
    new_student = Student(**student_data.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
) -> Student:
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Студента не знайдено")

    student.full_name = student_data.full_name
    student.specialty = student_data.specialty
    student.course = student_data.course
    student.group = student_data.group
    student.has_dormitory = student_data.has_dormitory

    db.commit()
    db.refresh(student)

    return student
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    # Усі ці рядки мають бути зміщені праворуч на 4 пробіли
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Студента не знайдено")

    db.delete(student)
    db.commit()

    return {"message": "Студента успішно видалено"}