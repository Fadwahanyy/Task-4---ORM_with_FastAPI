
from crud import get_all_students_in_course, get_all_courses_for_instructor
from db import SessionLocal
from models import Course, User

if __name__ == "__main__":
    
    with SessionLocal() as s:
        first_course = s.query(Course).first()
        first_instructor = s.query(User).filter_by(user_role="instructor").first()

    if first_course:
        students = get_all_students_in_course(first_course.id)
        print(f"Students in course '{first_course.title}':",
              [f"{u.first_name} {u.last_name}" for u in students])
    else:
        print("No course found. Run insert_data.py first.")

    if first_instructor:
        courses = get_all_courses_for_instructor(first_instructor.id)
        print(f"Courses for instructor {first_instructor.first_name}:",
              [c.title for c in courses])
    else:
        print("No instructor found. Run insert_data.py first.")
