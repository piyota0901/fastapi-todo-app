import datetime

from humps import camel  # type: ignore
from pydantic import UUID4, BaseModel


def _to_camel(string: str) -> str:
    return camel.case(string)


class Base(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = _to_camel
        allow_population_by_field_name = True


class TodoCreate(Base):
    title: str
    comment: str


class Todo(TodoCreate):
    id: UUID4
    is_done: bool = False
    create_at: datetime.datetime


class TodoDelete(Base):
    id: UUID4
