
from datetime import date
from sqlalchemy import select
from db import SessionLocal
from models import User, Student, Instructor, Course, Enrollment


def add_new_student(first_name: str, last_name: str, email: str, username: str | None = None,
                    gpa: float | None = None, school_name: str | None = None) -> User:
    with SessionLocal() as s, s.begin():
        u = User(first_name=first_name, last_name=last_name, email=email,
        username=username, user_role='student')
        s.add(u)
        s.flush()  
        s.add(Student(id=u.id, gpa=gpa, school_name=school_name))
        return u


def enroll_student_in_course(student_user_id: int, course_id: int,
                             status: str = "active", enrolled_date: date | None = None) -> Enrollment:
    with SessionLocal() as s, s.begin():
        existing = s.scalar(select(Enrollment).where(
            Enrollment.user_id == student_user_id,
            Enrollment.course_id == course_id
        ))
        if existing:
            return existing  

        e = Enrollment(user_id=student_user_id, course_id=course_id,
                       status=status, progress=0, completion_date=None)
        s.add(e)
        return e


def assign_grade(enrollment_id: int, grade_value: float) -> Enrollment | None:
    with SessionLocal() as s, s.begin():
        e = s.get(Enrollment, enrollment_id)
        if not e:
            return None
        e.final_grade = grade_value
        return e


def get_all_students_in_course(course_id: int) -> list[User]:
    with SessionLocal() as s:
        stmt = (
            select(User)
            .join(Enrollment, Enrollment.user_id == User.id)
            .where(Enrollment.course_id == course_id)
            .where(User.user_role == 'student')
            .order_by(User.first_name, User.last_name)
        )
        return list(s.scalars(stmt))


def get_all_courses_for_instructor(instructor_user_id: int) -> list[Course]:
    with SessionLocal() as s:
        stmt = (
            select(Course)
            .where(Course.instructor_id == instructor_user_id)
            .order_by(Course.title)
        )
        return list(s.scalars(stmt))
