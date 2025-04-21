from fastapi import FastAPI
import uvicorn
from typing import Optional

app = FastAPI()


# 查询参数
# ?page_index=1&page_size=18
@app.get('/users')
async def get_users(page_index: int,page_size: int):
    return {'page info': f'index: {page_index}, size:{page_size}'}

# 路径参数 + 查询参数
# http://127.0.0.1:8000/users/6/friends?page_index=9&page_size=16
@app.get('/users/{user_id}/friends') 
async def get_user_friends(page_index: int,user_id: int, page_size: Optional[int]=8): # 可选参数，默认值为8
    return {'user friends': f'user_id: {user_id}, index:{page_index}, size :{page_size}'}


if __name__ == '__main__':
    uvicorn.run('query:app', reload=True)
