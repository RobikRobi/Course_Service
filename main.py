from fastapi import FastAPI
from binascii import Error
from database.database import engine, Base
from models import UserModel, CourseModel, LessonModel

from courses.course_router import app as courses_app
from lessons.lessons_router import app as lessons_app




app = FastAPI(title="Course Service")

app.include_router(courses_app)
app.include_router(lessons_app)


@app.get("/get_db")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)     
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"True"})

