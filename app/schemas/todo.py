import datetime

from pydantic import UUID4, BaseModel


class TodoBase(BaseModel):
    title: str
    comment: str
    is_done: bool


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: UUID4
    create_at: datetime.datetime

    class Config:
        orm_mode = True
