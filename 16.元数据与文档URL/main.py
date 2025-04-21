from fastapi import FastAPI
import uvicorn

# 标题、描述和版本信息

title = 'My FastAPI learning project'
description = 'This is my first FastAPI learning project'
version = '1.0'
terms_of_service = 'www.baidu.com'
contact = {
    "name": "jack ma",
    'url':'http://hifengge.com',
    'email':'jk@fg.com'
}
license_info = { # 许可证协议
    "name": "Apache 2.0",
    "url":"https://www.apache.org"
}


# 定义api分类，一共两类，分别是 users 和 books
tags_metadata = [
    {
        "name": "books",
        "description": "APIs for book management.",
        "externalDocs":{ # 外部文档链接
            'description': "Books infor from external.",
            "url": "http://hifengge.com"
        }
    },
    {
        "name": "users",
        "description": "APIs for user management."
    }
]



app = FastAPI(title=title, description=description, version=version,
              terms_of_service=terms_of_service,
              contact=contact,
              license_info=license_info,
              openapi_tags= tags_metadata,
              openapi_url='/api/v1/json')


@app.post('/books',tags=['books','users'])
async def get_books():
    return {'book s': f"Here's all books information."}


@app.post('/users',tags=['users'])
async def get_users():
    return {"users": f"Here's all users information."}

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)