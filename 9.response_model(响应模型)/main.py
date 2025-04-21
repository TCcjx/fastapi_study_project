from enum import Enum
from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from pydantic import BaseModel, Field


users = {
    # "x": {"id": 0},
    "a": {"id": 1, "username": "a"},
    "b": {"id": 2, "username": "b", "password": "bbb"},
    "c": {"id": 3, "username": "c", "password": "ccc", "description": "default"},
    "d": {"id": 4, "username": "d", "password": "ddd", "description": "user ddd"},
    "e": {"id": 5, "username": "e", "password": "eee", "description": "user eee", "fullname": "Mary Water"}
}

app = FastAPI()


# response_model_exclude={"id"}
# response_model_include={"id", "username"}
# response_model_exclude_unset = True  设置了这个参数后代码,如果模型中，不带description参数就不会输出默认值，description有值时候才会输出
class UserOut(BaseModel):
    id: int
    username: str
    description: Optional[str]  = 'default'

# response_model 对客户端响应进行过滤设置
@app.get('/users/{username}', response_model=UserOut,response_model_exclude_unset=False) 
# 如果description没有赋值,则输出默认值
async def get_user(username: str):
    return users.get(username, {})

@app.get('/users',response_model = List[UserOut]) 
async def get_users():
    return users.values() # 返回字典的值




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)