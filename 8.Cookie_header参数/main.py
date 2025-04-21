from typing import Optional, Union
from enum import Enum

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from pydantic import BaseModel, Field

app = FastAPI() # 构建fastAPI应用



"""
1.Swagger UI 中的cookie由于浏览器的设置无法正常发送给客户端，
可以用Postman来进行测试，或者通过 response.set_cookie()来进行设置
2.Cookie和Header参数不能使用下划线，如果使用了下划线，可以通过alias取别名的方式来取代原用户名
"""

@app.put('/carts')
async def update_cart(*, response: Response,  # response: 返回给客户端的响应
                      favorite_schema: Optional[str] = Cookie(None, alias='favorite-schema')
                      ,api_token: str |  None = Header(None,alias='api-token')):

    result_dict = { 
        'favorite_schema': favorite_schema,
        'api_token': api_token
    }    

    response.set_cookie(key='favorite-schema', value='dark') 

    return result_dict
 
if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)
    
