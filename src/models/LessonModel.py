import datetime
import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from src.database.database import Base
from src.models.CourseModel import Course




if typing.TYPE_CHECKING:
    from src.models.CourseModel import Course


class Lesson(Base):
    __tablename__="lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    duration_minutes: Mapped[int] = mapped_column(default=40)
    is_open: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    course: Mapped["Course"] = relationship(back_populates="lessons")