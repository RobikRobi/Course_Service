from fastapi import FastAPI
from binascii import Error
from database.database import engine, Base
from models import UserModel, CourseModel



app = FastAPI(title="Course Service")


@app.get("/get_db")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)     
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"True"})