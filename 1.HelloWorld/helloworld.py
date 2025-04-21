from fastapi import FastAPI
import uvicorn # uvicorn：用于运行 FastAPI 应用的 ASGI 服务器
 
# 构建FastAPI应用
app = FastAPI()


@app.get('/')
async def helloworld2():
    return {'message': 'helloworld-2'}

@app.get('/helloworld')
async def helloworld():
    return {'message':'Hello world'}



if __name__ == '__main__':
    uvicorn.run('helloworld:app',reload=True,port=8000)