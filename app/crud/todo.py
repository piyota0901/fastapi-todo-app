from sqlalchemy.orm import Session

from app.models.todo import Todo as mTodo


def fetch_all(db: Session):
    return db.query(mTodo).all()
