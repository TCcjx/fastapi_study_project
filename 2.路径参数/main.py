import uvicorn 
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class Gender(str, Enum): # 字符串枚举类型
    male = 'male'
    female = 'female'


# 通过网址路径获取参数
# 定义api的顺序很重要
# fastapi 会讲路径参数自动转换函数中的参数类型
@app.get("/")
async def get():
    return {'user_id':'开始页面'}


@app.get('/users/current')
async def get_current_user():
    return {'user_id':'current_user_id'}


@app.get('/users/{user_id}')  # 路径参数
async def get_user(user_id:int): # 规定该路径参数为int类型
    return {'user': f'This is the user for {user_id}'}

@app.get('/students/{gender}')
async def get_user(gender: Gender):
    print(type(gender.value))
    return {'message': f'This is a {gender.value} student'}


if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)
