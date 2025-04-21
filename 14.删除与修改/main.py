from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, HTTPException, status, Depends
import uvicorn
from typing import Optional, List, Set, Union
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc, update
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


app = FastAPI()

def set_attrs(obj, data: dict):
    if data:
        for key, value in data.items():
            setattr(obj, key, value)


class Base(DeclarativeBase):
    pass

# 创建数据库引擎
engine = create_engine('mysql+mysqldb://root:123456@localhost/testdb', echo=True)  # 数据库引擎

# 定义数据库表结构
class StudentEntity(Base):
    __tablename__ = 'students'  

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # 设置成主键
    name: Mapped[str] = mapped_column(String(128), nullable= False, unique=True) # 不可为空
    gender: Mapped[str] = mapped_column(String(10), nullable=False) # 不可以为空

# 创建表，如果存在则不存在
Base.metadata.create_all(engine)
# 建立数据库会话
Session = sessionmaker(bind=engine)

# Define API models
class StudentBase(BaseModel):
    name: str
    gender:str

class StudentCreate(StudentBase):
    ...

class StudentUpdate(StudentBase):
    ...

class StudentOut(StudentBase):
    id: int

def get_db_session():
    db_session = Session()
    try:
        yield db_session # 创建数据库会话
    finally:
        db_session.close() # 请求处理完成后 关闭会话

# 查询学生信息
@app.get('/students', response_model=List[StudentOut]) 
async def get_students(db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).order_by(asc(StudentEntity.name)) # 升序查询学生实体信息
    return db_session.execute(query).scalars().all()

# 创建学生信息
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

# 修改学生信息
@app.put('/students/{student_id}',response_model=StudentOut)
async def update_student(*, student_id: int = Path(...), student: StudentUpdate, db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).where(StudentEntity.id == student_id)
    exist_student = db_session.execute(query).scalar()
    if not exist_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'{student_id} not found.')
    
    # update_query = update(StudentEntity).values(student.model_dump()).where(StudentEntity.id == student_id)
    # db_session.execute(update_query)

    # exist_student.name = student.name
    # exist_student.gender = student.gender

    set_attrs(exist_student, student.model_dump())
    db_session.commit()
    return exist_student

# 删除学生信息
@app.delete('/students/{student_id}', response_model=StudentOut)
async def delete_student(student_id: int = Path(...), db_session: Session = Depends(get_db_session)):
  query = select(StudentEntity).where(StudentEntity.id == student_id)
  exist_student = db_session.execute(query).scalar()
  if not exist_student:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'{student_id} not found.')
  db_session.delete(exist_student)
  db_session.commit( )
  return exist_student 





if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)