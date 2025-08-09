
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from db import engine


metadata = MetaData()
metadata.reflect(bind=engine, schema="public")   


AutomapBase = automap_base(metadata=metadata)
AutomapBase.prepare()


User        = AutomapBase.classes.users
Admin       = AutomapBase.classes.admins
Student     = AutomapBase.classes.students
Instructor  = AutomapBase.classes.instructors
Course      = AutomapBase.classes.courses
Enrollment  = AutomapBase.classes.enrollments
Assignment  = AutomapBase.classes.assignments
Submission  = AutomapBase.classes.submissions

#
Base = AutomapBase
