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
    is_done: bool = False


class Todo(TodoCreate):
    id: str
    create_at: datetime.datetime
    updated_at: datetime.datetime
    
    def __eq__(self, other: object):
        if not isinstance(other, Todo):
            return NotImplemented
        return self.id == other.id

class TodoUpdate(Base):
    title: str
    description: str
    is_done: bool

class TodoDelete(Base):
    id: UUID4
