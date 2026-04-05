from typing import Optional, List
from sqlalchemy import select, desc, asc, or_
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import get_session
from models.CourseModel import Course
from shemas.course_shema import CreateCourse, ResponseCourse, UpdateCourse
from shemas.lesson_shema import ResponseLesson
from models.CourseEnum import CoursesCategory, CoursesLevel




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
@app.get("/get_courses_all")
async def get_courses(session:AsyncSession = Depends(get_session)):
    courses = await session.scalars(select(Course))
    return courses.all()

@app.get("/get_courses", response_model=List[ResponseCourse])
async def get_courses(# Фильтры
        category: Optional[CoursesCategory] = None,
        level: Optional[CoursesLevel] = None,
        is_published: Optional[bool] = Query(True), # По умолчанию показываем опубликованные
        search: Optional[str] = None,
        
        # Сортировка и пагинация
        sort_by: str = Query("created_at", enum=["created_at", "title"]),
        sort_order: str = Query("desc", enum=["asc", "desc"]),
        limit: int = Query(10, gt=0, le=100),
        offset: int = Query(0, ge=0),
        
        session: AsyncSession = Depends(get_session)
    ):
        # 1. Базовый запрос
        query = select(Course)

        # 2. Динамические фильтры
        if category:
            query = query.where(Course.category == category)
        
        if level:
            query = query.where(Course.level == level)
            
        if is_published is not None:
            query = query.where(Course.is_published == is_published)

        if search:
            # Поиск по подстроке в названии (регистронезависимый в PostgreSQL через ilike)
            query = query.where(Course.title.ilike(f"%{search}%"))

        # 3. Логика сортировки
        sort_attr = getattr(Course, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_attr))
        else:
            query = query.order_by(asc(sort_attr))

        # 4. Пагинация (лимит и смещение)
        query = query.limit(limit).offset(offset)

        # 5. Выполнение
        result = await session.execute(query)
        courses = result.scalars().all()

        return courses

# Получение курса по id
@app.get("/get_course/{course_id}", response_model=ResponseCourse)
async def get_course_id(course_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Course).options(selectinload(Course.lessons)).where(Course.id == course_id)
    result = await session.execute(query)
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

# Получение всех уроков курса
@app.get("/courses/{course_id}/lessons", response_model=list[ResponseLesson])
async def get_course_lessons(course_id: int, session: AsyncSession = Depends(get_session)):
    query = (
        select(Course)
        .options(selectinload(Course.lessons))
        .where(Course.id == course_id)
    )
    result = await session.execute(query)
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course.lessons


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