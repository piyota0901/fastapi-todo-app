from pydantic import UUID4
from sqlalchemy.orm import Session

from backend.models.todo import Todo
from backend.schemas import todo


def fetch_all(db: Session):
    return db.query(Todo).all()


def fetch_by_id(db: Session, todo_id: UUID4):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def add(db: Session, new_todo: todo.TodoCreate):
    create_todo = Todo(title=new_todo.title, comment=new_todo.comment)
    db.add(create_todo)
    db.commit()
    db.refresh(create_todo)
    return create_todo


def delete_by_id(db: Session, todo_id: UUID4):
    todo = db.query(Todo).filter(Todo.id == todo_id)
    todo.delete()
    db.commit()
    return
