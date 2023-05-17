import datetime

from humps import camel  # type: ignore
from pydantic import UUID4, BaseModel


def _to_camel(string: str) -> str:
    return camel.case(string)


class TodoBase(BaseModel):
    title: str
    comment: str

    class Config:
        orm_mode = True
        alias_generator = _to_camel
        allow_population_by_field_name = True


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: UUID4
    is_done: bool
    create_at: datetime.datetime
