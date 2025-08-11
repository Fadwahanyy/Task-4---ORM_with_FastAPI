from datetime import date
from sqlalchemy import select, and_
from db import SessionLocal
from models import User, Student, Instructor, Course, Enrollment, Assignment



def get_or_create_user_student(first, last, email, username, *, gpa=None, school_name=None) -> User:
    
    with SessionLocal() as s, s.begin():
        u = s.scalar(select(User).where(User.email == email))
        if not u:
            u = User(first_name=first, last_name=last, email=email,
                     username=username, user_role="student")
            s.add(u); s.flush() 
            s.add(Student(id=u.id, gpa=gpa, school_name=school_name))
        return u

def get_or_create_instructor(first, last, email, username, *, specialization=None, department=None) -> User:
    
    with SessionLocal() as s, s.begin():
        u = s.scalar(select(User).where(User.email == email))
        if not u:
            u = User(first_name=first, last_name=last, email=email,
                     username=username, user_role="instructor")
            s.add(u); s.flush()
            s.add(Instructor(id=u.id, specialization=specialization, department=department))
        return u

def get_or_create_course(title, instructor_id, *, description=None, category=None,
                         start_date=None, end_date=None, is_deleted=False) -> Course:
    
    with SessionLocal() as s, s.begin():
        c = s.scalar(
            select(Course).where(
                and_(Course.title == title, Course.instructor_id == instructor_id)
            )
        )
        if not c:
            c = Course(
                title=title, description=description, category=category,
                start_date=start_date, end_date=end_date,
                instructor_id=instructor_id, is_deleted=is_deleted
            )
            s.add(c)
        return c

def get_or_create_enrollment(student_user_id: int, course_id: int, *, status="active") -> Enrollment:
   
    with SessionLocal() as s, s.begin():
        e = s.scalar(
            select(Enrollment).where(
                and_(Enrollment.user_id == student_user_id, Enrollment.course_id == course_id)
            )
        )
        if not e:
            e = Enrollment(user_id=student_user_id, course_id=course_id, status=status, progress=0)
            s.add(e)
        return e

def get_or_create_assignment(course_id: int, title: str, *, description=None, due_date=None, max_score=None) -> Assignment:

    with SessionLocal() as s, s.begin():
        a = s.scalar(
            select(Assignment).where(
                and_(Assignment.course_id == course_id, Assignment.title == title)
            )
        )
        if not a:
            a = Assignment(course_id=course_id, title=title, description=description,
                           due_date=due_date, max_score=max_score)
            s.add(a)
        return a

def assign_final_grade(enrollment_id: int, grade_value: float) -> None:
    
    with SessionLocal() as s, s.begin():
        e = s.get(Enrollment, enrollment_id)
        if e:
            e.final_grade = grade_value



if __name__ == "__main__":
   
    inst = get_or_create_instructor(
        "Sara", "Mostafa", "sara@gmail.com", "sara",
        specialization="Databases", department="CS"
    )

   
    course = get_or_create_course(
        "Intro to Databases", inst.id,
        description="ERD & SQL", category="CS",
        start_date=date(2025, 9, 1), end_date=date(2025, 12, 20)
    )

   
    student = get_or_create_user_student(
        "Omar", "Ali", "omar@gmail.com", "omar",
        gpa=3.5, school_name="NU"
    )

    enrollment = get_or_create_enrollment(student.id, course.id, status="active")

   
    get_or_create_assignment(course.id, "HW1", description="Design an ERD", due_date=date(2025, 10, 1), max_score=100)
    assign_final_grade(enrollment.id, 95.0)

    print("Idempotent seed complete.")
