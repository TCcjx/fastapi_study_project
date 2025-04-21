from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, HTTPException, status, Depends
import uvicorn
from typing import Optional, List, Set, Union
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc, update
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


app = FastAPI()


class Base(DeclarativeBase):
    pass

# 数据库引擎
engine = create_engine('mysql+mysqldb://root:123456@localhost/testdb', echo=True)  # 数据库引擎

class StudentEntity(Base):
    __tablename__ = 'students'  

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # 设置成主键
    name: Mapped[str] = mapped_column(String(128), nullable= False, unique=True) # 不可为空
    gender: Mapped[str] = mapped_column(String(10), nullable=False) # 不可以为空

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Define API models
class StudentBase(BaseModel):
    name: str
    gender:str

class StudentCreate(StudentBase):
    ...

class StudentOut(StudentBase):
    id: int

def get_db_session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()

# 查询学生名单
@app.get('/students', response_model=List[StudentOut]) 
async def get_students(db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).order_by(asc(StudentEntity.name)) # 升序
    return db_session.execute(query).scalars().all()

# 添加学生信息
@app.post('/students',response_model=StudentOut)
async def create_student(student: StudentCreate, db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).where(StudentEntity.name == student.name)  #  定义查询
    records = db_session.execute(query).scalars().all() 
    if records: # 如果该名字的学生已经存在，则报400错误
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'{student.name} already exists.') # 错误请求
    student_entity = StudentEntity(name=student.name, gender=student.gender)
    db_session.add(student_entity)
    db_session.commit( )

    return student_entity

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)