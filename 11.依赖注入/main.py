from typing import Optional, List, Set, Union
import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# 设置全局依赖
async def set_charset():
    print('set UTF-8')

app = FastAPI(dependencies=[Depends(set_charset)]) # 这个依赖对全局生效


# 验证是否经过用户授权
async def verify_auth(api_token: Optional[str] = Header(None, alias="api-token")):
    if not api_token:
        raise HTTPException(status_code=400, detail="Unauthorized")

def total_param(total_params: Optional[int] = 2):
    return total_params


class Page_info:
    def __init__(self, page_index : Optional[int] = 1, page_size: Optional[int] = 8):
        self.page_index = page_index
        self.page_size = page_size

def pageinfo_params(page_index: Optional[int] = 1, page_size: Optional[int] = 10, page_total: Optional[int] = Depends(total_param)):
    return {'page_index':page_index,"page_size":page_size,'page_total':page_total}
    

@app.get('/items')
async def get_items(page_info: dict = Depends(pageinfo_params)):
    return {'page_index': page_info.get("page_index"), 'page_size': page_info.get('page_size'),
    'page_total': page_info.get('page_total')}


@app.get('/user',dependencies=[Depends(verify_auth)]) # 注解中添加依赖，在处理请求之前会先调用依赖,如果未通过校验，则不会继续执行请求
async def get_items(page_info: dict = Depends(pageinfo_params)):
    return {'page_index': page_info.get('page_index'),'page_size':page_info.get('page_size')}


@app.get('/users')
async def get_items(page_info: Page_info = Depends(Page_info)): # 返回一个Page_info类的一个实例
    return {'page_index': page_info.page_index,'page_size': page_info.page_size}



if __name__ == '__main__':
     uvicorn.run('main:app',reload=True)
