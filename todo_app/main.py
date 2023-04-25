from datetime import datetime

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    id: int
    title: str
    comment: str
    isDone: bool
    create_at: str


class AddTodo(BaseModel):
    title: str
    comment: str


db = [
    Todo(id=1, title="sample1", comment="sample1です。", isDone=False, create_at="2023-04-25"),
    Todo(id=2, title="sample2", comment="sample2です。", isDone=False, create_at="2023-04-25"),
    Todo(id=3, title="sample3", comment="sample3です。", isDone=False, create_at="2023-04-25"),
]


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.get("/todo/{todo_id}")
async def featch_by_id(todo_id: int) -> Todo:
    todo = list(filter(lambda todo: todo.id == todo_id, db))[0]
    return todo


@app.get("/todo/")
async def fetch_all() -> list[Todo]:
    return db


@app.post("/todo/")
async def add(todo: AddTodo):
    max_id = max([t.id for t in db])
    create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_todo = Todo(id=max_id + 1, title=todo.title, comment=todo.comment, isDone=False, create_at=create_at)
    db.append(new_todo)
    # JSONResponse利用時はシリアライズする必要がある
    # https://fastapi.tiangolo.com/ja/advanced/additional-status-codes/
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_todo.dict())
