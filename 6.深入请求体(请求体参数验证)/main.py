from enum import Enum
from typing import Optional, List, Set

import uvicorn
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Address(BaseModel):
    address: str = Field(..., examples=["5 Queens Street"])
    postcode: str = Field(..., examples=["0765"])

    model_config = { # 设置默认值 优先级 > Field, Body检验项里面默认值的优先级最高
        "json_schema_extra": {
            "examples": [{
                "address": "2 Queens Street",
                "postcode": "0987"
            }]
        }
    }


class User(BaseModel):
    username: str = Field(..., min_length=3) # 必须参数
    description: Optional[str] = Field(None, max_length=10) # 可选类型，可以是None
    address: Address


class Feature(BaseModel):
    name: str


class Item(BaseModel):
    name: str
    length: int
    features: List[Feature]

# 加上*，让后面的参数全部变成关键字参数 
def add(*, num1: int, num2: int):
    return num1 + num2  

 
print(add(num1=1, num2=2))


# count: int = Body(..., ge=2, examples=[8]) 将 count 也添加进请求体，并进行参数校验
@app.put('/carts/{cart_id}')
async def update_cart(*, cart_id: int, user: User = Body(...,examples=[{"username": "Smith","address":{"address":'北京市朝阳区',"postcode":'9876'}}]), item: Item, count: int = Body(..., ge=2, examples=[8])):
    print(user.username)
    print(item.name)
    result_dict = {
        "cartid": cart_id,  
        "username": user.username,
        "itemname": item.name,
        "count": count
    }

    return result_dict


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)