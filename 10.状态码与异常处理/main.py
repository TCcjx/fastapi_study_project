import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response, Request, HTTPException, status

from typing import Optional, Union, List
from enum import Enum
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse

users = {
    # "x": {"id": 0},
    "a": {"id": 1, "username": "a"},
    "b": {"id": 2, "username": "b", "password": "bbb"},
    "c": {"id": 3, "username": "c", "password": "ccc", "description": "default"},
    "d": {"id": 4, "username": "d", "password": "ddd", "description": "user ddd"},
    "e": {"id": 5, "username": "e", "password": "eee", "description": "user eee", "fullname": "Mary Water"}
}

app = FastAPI()


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    fullname: Optional[str] = None
    description: Optional[str] = None

class UserIn(UserBase):
    password: str 

class UserOut(UserBase):
    ... # Python中特殊的对象，通常用作占位符 


class UserNotFoundException(Exception):
    def __init__(self, username:str):
        self.username = username

class ErrorMessage(BaseModel):
    error_code: int
    message: str


# 异常处理
@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
        'error_code': 404,
        'message': f'{exc.username} not found',
        'info': '报错啦'
    })

# response_model 响应模型
@app.post('/users', status_code=201, response_model=UserOut, responses={
    400: {'model':ErrorMessage},
    401: {'model':ErrorMessage}  # HTTP响应
})
async def create_user(user: UserIn):
    if users.get(user.username,None):   
        error_messsage = ErrorMessage(error_code=400,message=f'{user.username} already exists.')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_messsage.model_dump()) 
    user_dict = user.model_dump()
    user_dict.update({'id' : 9})
    return user_dict

@app.get('/users/{username}', status_code=200, response_model=UserOut)
async def get_user(username:  str = Path(..., max_length=3)):
    user = users.get(username,None)
    if user: # user为None，则跳过
        return user
    # print(status.HTTP_404_NOT_FOUND) 其实就是404  
    # raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='username not found')
    raise UserNotFoundException(username)

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)