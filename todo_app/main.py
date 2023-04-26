from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    id: UUID
    title: str
    comment: str
    isDone: bool
    create_at: str


class AddTodo(BaseModel):
    title: str
    comment: str


db = [
    Todo(
        id=UUID("2ae9a1d9-20b0-4962-9754-d8f6972e425f"),
        title="sample1",
        comment="sample1です。",
        isDone=False,
        create_at="2023-04-25",
    ),
    Todo(
        id=UUID("d8b45d0a-0419-4798-8f36-2603ef588ab7"),
        title="sample2",
        comment="sample2です。",
        isDone=False,
        create_at="2023-04-25",
    ),
    Todo(
        id=UUID("d35a6b0c-2ce7-4992-9f73-a5ac2a121797"),
        title="sample3",
        comment="sample3です。",
        isDone=False,
        create_at="2023-04-25",
    ),
]


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.get("/todo/{todo_id}")
async def featch_by_id(todo_id: UUID) -> Todo:
    todo = list(filter(lambda todo: todo.id == todo_id, db))[0]
    return todo


@app.get("/todo/")
async def fetch_all() -> list[Todo]:
    return db


@app.post("/todo/")
async def add(todo: AddTodo):
    create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_todo = Todo(id=uuid4(), title=todo.title, comment=todo.comment, isDone=False, create_at=create_at)
    db.append(new_todo)
    # JSONResponse利用時はシリアライズする必要がある
    # https://fastapi.tiangolo.com/ja/advanced/additional-status-codes/
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_todo.dict())
