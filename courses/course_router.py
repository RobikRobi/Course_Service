from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import get_session
from models.CourseModel import Course
from courses.shemas import CreateCourse, ResponseCourse, UpdateCourse

app = APIRouter(prefix="/courses", tags=["Courses"])

# Создание курса
@app.post("/create")
async def create_courses(data: CreateCourse, session:AsyncSession = Depends(get_session)):
    new_course = Course(**data.model_dump())
    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)
    
    return new_course

# Получение всех курсов
@app.get("/get_courses")
async def get_courses(session:AsyncSession = Depends(get_session)):
    courses = await session.scalars(select(Course))
    return courses.all()

# Получение курса по id
@app.get("/get_course/{course_id}", response_model=ResponseCourse)
async def get_course_id(course_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Course).options(selectinload(Course.lessons)).where(Course.id == course_id)
    result = await session.execute(query)
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

# Редактирование курса
@app.put("/update/{course_id}", response_model=ResponseCourse)
async def update_course(data: UpdateCourse, course_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Course)
        .options(selectinload(Course.lessons))
        .where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)

    await session.commit()
    await session.refresh(course)

    return course

# Удаление курса
@app.delete("/delete/{course_id}")
async def delete_course(course_id: int, session: AsyncSession = Depends(get_session)):
    course = await session.scalar(select(Course).where(Course.id == course_id))
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await session.delete(course)
    await session.commit()

    return {"message": f"Course with ID {course_id} has been deleted"}