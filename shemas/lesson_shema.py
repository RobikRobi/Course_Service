import datetime
from pydantic import BaseModel



class CreateLesson(BaseModel):
    course_id: int
    title: str
    summary: str
    position: int
    duration_minutes: int


class ResponseLesson(BaseModel):
    id: int
    course_id: int
    title: str
    summary: str
    position: int
    duration_minutes: int
    is_open: bool
    created_at: datetime.datetime


class UpdateLesson(BaseModel):
    title: str | None
    summary: str | None
    position: int | None
    duration_minutes: int | None
    is_open: bool