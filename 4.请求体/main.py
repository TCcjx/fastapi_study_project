from enum import Enum
from typing import  Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI() # 构建FastAPI应用

class Gender(str, Enum): # 枚举类型
    male = "male"
    female = "female"

# 定义请求体类型s
# 请求体
class UserModel(BaseModel):
    username: str
    description: Optional[str] = 'default' # 可选字符串，缺省值为default
    gender: Gender  

# POST请求 
# 创建用户
@app.post('/users')
async def create_user(usermodel: UserModel):
    # print(usermodel.username,usermodel.description)
    user_dict = usermodel.model_dump() # 返回json数据
    return user_dict

 
# 当需要修改用户的时候用PUT请求
@app.put('/users/{user_id}') # user_id 是 路径参数
async def update_user(user_id: int, usermodel: UserModel):
    user_dict = usermodel.model_dump()
    user_dict.update({'id':user_id}) # 更新字典 json数据
    return user_dict    

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)

