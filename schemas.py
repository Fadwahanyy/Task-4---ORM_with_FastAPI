from pydantic import BaseModel, EmailStr 
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True



class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    class Config:
        orm_mode = True



class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int
    status: str

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    class Config:
        orm_mode = True



class AssignmentBase(BaseModel):
    course_id: int
    title: str
    due_date: date

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentOut(AssignmentBase):
    id: int
    class Config:
        orm_mode = True



class SubmissionBase(BaseModel):
    assignment_id: int
    user_id: int
    file_url: str
    grade: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(SubmissionBase):
    id: int
    class Config:
        orm_mode = True
