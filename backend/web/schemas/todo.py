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
    description: str


class Todo(TodoCreate):
    id: str
    is_done: bool = False
    create_at: datetime.datetime
    updated_at: datetime.datetime

class TodoUpdate(Base):
    id: str
    title: str
    description: str
    is_done: bool

class TodoDelete(Base):
    id: UUID4
