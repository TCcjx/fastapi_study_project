from fastapi import FastAPI, Path, Query
import uvicorn
from pydantic import BaseModel
from typing import Optional
from enum import Enum


app = FastAPI() # 创建FastAPI应用

class Gender(str, Enum): # 枚举类型
    male = 'male'
    female = 'female'

# 定义请求体类型
# 请求体
class UserModel(BaseModel):
    username: str
    description: Optional[str] = 'default' # 可选字符串，缺省值为default
    gender: Gender  

'''
Path(..., title='User ID', gt=0, le=1000)：使用 Path 函数对 user_id 进行验证和添加元数据：
...：表示该参数是必需的。(PATH的默认参数只能是...，表示必选参数)
title='User ID'：为参数添加标题，用于文档生成。
gt=0：表示 user_id 必须大于 0。
le=1000：表示 user_id 必须小于或等于 1000。
'''


# 路径参数和查询参数都支持 参数验证
#  Path(..., title='User ID', ge = 0,le = 1000)  含义为 必选参数｜大于等于0｜小于等于1000
@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(..., title='User ID', ge = 0,le = 1000)):
    return {'user': f'This is the user for {user_id}'}

# Query(1,alias='page-index',title='Page index',ge = 1) 含义为 默认值为1｜别名 page-index｜大于等于1
@app.get('/users')
async def get_user(page_index: int = Query(1,alias='page-index',title='Page index',ge = 1)):
    return {'users' : f'page index: {page_index}'}


if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)