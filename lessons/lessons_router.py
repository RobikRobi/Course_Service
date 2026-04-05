from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import get_session
from models.LessonModel import Lesson
from shemas.lesson_shema import CreateLesson, ResponseLesson, UpdateLesson




app = APIRouter(prefix="/lessons", tags=["Lessons"])

# Создание урока
@app.post("/create")
async def create_lesson(data: CreateLesson, session:AsyncSession = Depends(get_session)):
    new_lesson = Lesson(**data.model_dump())
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    
    return new_lesson

# Получение урока по id
@app.get("/get_lesson/{lesson_id}", response_model=ResponseLesson)
async def get_lesson_id(lesson_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Lesson).options(selectinload(Lesson.course)).where(Lesson.id == lesson_id)
    result = await session.execute(query)
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return lesson

# Редактирование урока
@app.put("/update/{lesson_id}", response_model=ResponseLesson)
async def update_course(data: UpdateLesson, 
                        lesson_id: int, 
                        session: AsyncSession = Depends(get_session)):
    
    result = await session.execute(
        select(Lesson)
        .options(selectinload(Lesson.course))
        .where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lesson, key, value)

    await session.commit()
    await session.refresh(lesson)

    return lesson

# Удаление урока
@app.delete("/delete/{course_id}")
async def delete_lesson(lesson_id: int, session: AsyncSession = Depends(get_session)):
    lesson = await session.scalar(select(Lesson).where(Lesson.id == lesson_id))
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    await session.delete(lesson)
    await session.commit()

    return {"message": f"Lesson with ID {lesson_id} has been deleted"}