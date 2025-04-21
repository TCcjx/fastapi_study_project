from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc, update
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


class Base(DeclarativeBase): # 数据库基类
    pass

# 创建一个 SQLAlchemy 引擎，用于连接 MySQL 数据库。连接字符串包含用户名、密码、主机和数据库名称。
engine = create_engine('mysql+mysqldb://root:123456@localhost/testdb', echo=True)


# 定义数据库表结构
class StudentEntity(Base):
    __tablename__ = 'students'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False) 

Base.metadata.create_all(engine) # 创建表，如果存在，则不再创建
Session = sessionmaker(bind=engine) # 定义一个数据库会话
app = FastAPI() # 创建一个FastAPI应用程序实例

# define API Model

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
