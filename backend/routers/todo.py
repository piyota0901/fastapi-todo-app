from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from backend.crud import todo
from backend.db.session import SessionLocal
from backend.schemas import todo as sTodo

# https://fastapi.tiangolo.com/ja/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(prefix="/todo", tags=["todo"], responses={404: {"description": "Not found"}})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/todos", response_model=list[sTodo.Todo])
def get_todo_all(db: Session = Depends(get_db)):
    todos = todo.fetch_all(db=db)
    return todos


@router.get("/{todo_id}", response_model=sTodo.Todo)
def get_todo_by_id(todo_id: UUID4, db: Session = Depends(get_db)):
    t = todo.fetch_by_id(db=db, todo_id=todo_id)
    return t


@router.post("/", response_model=sTodo.Todo)
def create_todo(new_todo: sTodo.TodoCreate, db: Session = Depends(get_db)):
    created_todo = todo.add(db=db, new_todo=new_todo)
    return created_todo


@router.delete("/todo")
def delete_todo_by_id(todo_id: UUID4, db: Session = Depends(get_db)):
    try:
        todo.delete_by_id(db=db, todo_id=todo_id)
    except Exception:
        return {"message": "success"}
