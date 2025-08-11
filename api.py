
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List

from db import SessionLocal, engine
import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LMS API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = db.scalar(select(models.User).where(models.User.email == user.email))
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists.")
    obj = models.User(**user.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.User, user_id)
    if not obj:
        raise HTTPException(404, "User not found.")
    db.delete(obj); db.commit()
    return {"message": "User deleted."}


@app.post("/courses", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    obj = models.Course(**course.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/courses", response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@app.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Course, course_id)
    if not obj:
        raise HTTPException(404, "Course not found.")
    for k, v in course.dict().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj


@app.post("/enrollments", response_model=schemas.EnrollmentOut, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
   
    if not db.get(models.User, enrollment.user_id):
        raise HTTPException(404, "User not found.")
    if not db.get(models.Course, enrollment.course_id):
        raise HTTPException(404, "Course not found.")
    dup = db.scalar(
        select(models.Enrollment).where(
            and_(models.Enrollment.user_id == enrollment.user_id,
                 models.Enrollment.course_id == enrollment.course_id)
        )
    )
    if dup:
        raise HTTPException(400, "User already enrolled in this course.")
    obj = models.Enrollment(**enrollment.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@app.post("/assignments", response_model=schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    if not db.get(models.Course, assignment.course_id):
        raise HTTPException(404, "Course not found.")
    obj = models.Assignment(**assignment.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/assignments/{course_id}", response_model=List[schemas.AssignmentOut])
def list_assignments_for_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()


@app.post("/submissions", response_model=schemas.SubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_assignment(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    if not db.get(models.Assignment, submission.assignment_id):
        raise HTTPException(404, "Assignment not found.")
    if not db.get(models.User, submission.user_id):
        raise HTTPException(404, "User not found.")
    obj = models.Submission(**submission.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.put("/submissions/{submission_id}/grade", response_model=schemas.SubmissionOut)
def grade_submission(submission_id: int, grade: str = Query(...), db: Session = Depends(get_db)):
    obj = db.get(models.Submission, submission_id)
    if not obj:
        raise HTTPException(404, "Submission not found.")
    obj.grade = grade
    db.commit(); db.refresh(obj)
    return obj
