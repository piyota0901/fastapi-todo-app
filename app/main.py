from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud import todo
from app.db.session import SessionLocal
from app.schemas import todo as sTodo

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos/", response_model=list[sTodo.Todo])
def get_todo_all(db: Session = Depends(get_db)):
    todos = todo.fetch_all(db=db)
    return todos


# class Todo(BaseModel):
#     id: UUID
#     title: str
#     comment: str
#     isDone: bool
#     create_at: str


# class AddTodo(BaseModel):
#     title: str
#     comment: str


# @app.get("/ping")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/todo/{todo_id}")
# async def featch_by_id(todo_id: UUID) -> Todo:
#     todo = list(filter(lambda todo: todo.id == todo_id, db))[0]
#     return todo


# @app.get("/todo/")
# async def fetch_all() -> list[Todo]:
#     return db


# @app.post("/todo/")
# async def add(todo: AddTodo):
#     create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     new_todo = Todo(id=uuid4(), title=todo.title, comment=todo.comment, isDone=False, create_at=create_at)
#     db.append(new_todo)
#     # JSONResponse利用時はシリアライズする必要がある
#     # https://fastapi.tiangolo.com/ja/advanced/additional-status-codes/
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_todo.dict())
