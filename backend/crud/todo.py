from fastapi import HTTPException, status
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


def update(db: Session, update_todo: todo.Todo):
    query = db.query(Todo).filter(Todo.id == update_todo.id)
    db_todo = query.first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{update_todo.id} is not found.")
    # https://fastapi.tiangolo.com/ja/tutorial/body-updates/#pydanticexclude_unset
    update_data = update_todo.dict(exclude_unset=True)
    update_data.pop("create_at")
    query.filter(Todo.id == update_todo.id).update(values=update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_todo)
    return db_todo
