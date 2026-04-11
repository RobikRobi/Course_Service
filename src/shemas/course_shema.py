import datetime
from pydantic import BaseModel
from src.models.CourseEnum import CoursesCategory, CoursesLevel



class CreateCourse(BaseModel):
    title: str
    description: str
    category: CoursesCategory | None
    level: CoursesLevel | None


class ResponseCourse(BaseModel):
    id: int
    title: str
    description: str
    category: CoursesCategory | None
    level: CoursesLevel | None
    is_published: bool
    created_at: datetime.datetime

class UpdateCourse(BaseModel):
    title: str | None
    description: str | None
    category: CoursesCategory | None
    level: CoursesLevel | None
    is_published: bool