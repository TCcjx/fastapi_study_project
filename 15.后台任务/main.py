from enum import  Enum

import uvicorn
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

# 模拟需要执行的后台任务
def send_message(message: str):

    print(f'Start sending "{message}"')
    time.sleep(100)
    print(f'Complete sending "{message}"')
    return True


# 将需要执行的任务添加到后台，然后返回信息，等待后台任务的执行。
@app.post('/notify')
async def send_notification(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message=message) # 添加到后台任务

    return {"message": f"Sending notification {message} in background successful."}



if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)