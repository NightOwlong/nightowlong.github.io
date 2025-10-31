import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# 读取数据
with open("./data/works.json") as fp:
    data: dict = json.loads(fp.read())

def save():
    with open("./data/works.json", "w") as fp:
        fp.write(json.dumps(data))

def refresh():
    for index in range(len(data["data"])):
        data["data"][index]["id"] = index

app = FastAPI(
    title="HomeWork",
    version="0.0.1",
    description="an application to check the homework"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.get("/")
async def home():
    return {
        "msg": "Welcome to Homework"
    }

class Work(BaseModel):
    create: str
    title: str
    description: str
    deadline: str

    def show(self):
        return {
            "id": len(data["data"]) + 1,
            "create": self.create,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline
        }

@app.post("/api/add")
async def add(work: Work):
    data["data"].append(work.show())
    save()
    return {
        "status": "ok.",
    }

class Delete(BaseModel):
    id: int

@app.delete("/api/delete")
async def delete(dele: Delete):
    id = dele.id
    position = None
    for index in range(len(data["data"])):
        if data["data"][index]["id"] == id:
            position = index
            break
    if position != None:
        del data["data"][position]
        refresh()
        save()
        return {
            "status": "ok."
        }
    else:
        return {
            "status": "err to delete this ID"
        }
    
@app.get("/api/search")
async def search():
    return {
        "status": "ok.",
        "data": data
    }

@app.get("/student")
async def student():
    with open("./html/student.html") as fp:
        return HTMLResponse(fp.read())
    
@app.get("/admin")
async def admin():
    with open("./html/admin.html") as fp:
        return HTMLResponse(fp.read())


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
