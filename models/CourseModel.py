import typing
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, Enum
from database.database import Base
from models.CourseEnum import CoursesCategory, CoursesLevel





if typing.TYPE_CHECKING:
    from models.LessonModel import Lesson


class Course(Base):
    __tablename__="courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[CoursesCategory] = mapped_column(Enum(CoursesCategory), default=None)
    level: Mapped[CoursesLevel] = mapped_column(Enum(CoursesLevel), default=None)
    is_published: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="course",  
                                                   cascade="all, delete-orphan")