from datetime import date, timedelta, timezone, datetime
from math import exp
from typing import Optional, List, Set, Union
from unittest import expectedFailure

from click import get_current_context
from httpcore import TrioBackend
import jwt
import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
# from sqlalchemy import create_engine, String, Integer, select
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


SECURITY_KEY = "ioweurlaksjdfoiquwerlkasjdf"
ALGORITHMS = "HS256"
'''
在 FastAPI 中，OAuth2PasswordBearer 是一个用于处理 OAuth2 密码模式的依赖项。
它主要用于从 HTTP 请求的 Authorization 头部中提取令牌（通常是 Bearer 令牌），并验证其有效性
'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # 提取令牌token

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI()

def validate_user(username: str, password: str):
    if username == 'jack' and password == '111':
        return username  # 通过信息验证
    return None # 未通过验证

# 获取JWT令牌
def get_current_username(token: str = Depends(oauth2_scheme)):
    unauth_exp = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'Unauthorized')
    try:    
        username = None 
        token_data = jwt.decode(token,SECURITY_KEY, ALGORITHMS)
        if token_data:
           username = token_data.get('username', None)
    except Exception as error:
        raise unauth_exp
    
    if not username: # 如果用户不存在，则报异常。
        raise unauth_exp
        
    return username 

# 登陆功能
'''
在 FastAPI 中，OAuth2PasswordRequestForm 是一个特殊的依赖项，
用于处理 OAuth2 密码模式的登录请求。它从请求体中提取用户名和密码，
并将它们作为参数传递给路由处理函数。
'''
@app.post('/token')
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(login_form.username, login_form.password) 
    if not username:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail= 'Incorrect username or password',
                             headers='headers={"WWW-Authenticate": "Bearer"}')
    
    token_expires = datetime.now(timezone.utc) + timedelta(seconds=80)
    token_data = {
        "username": username,
        "exp": token_expires # 失效时间
    }
    token = jwt.encode(token_data.copy( ), SECURITY_KEY, algorithm=ALGORITHMS) # 进行加密
    return Token(access_token= token, token_type='bearer')



@app.get('/items')
async def get_items(username: str = Depends(get_current_username)):
    return {"current user": username}


if __name__ == '__main__':
   uvicorn.run('main:app', reload=True)