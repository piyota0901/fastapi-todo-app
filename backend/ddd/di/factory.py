from backend.ddd.application.todo_application import TodoApplicationService
from backend.ddd.infrastructure.repositories.transaction import (
    UnitOfWork,
)


def get_todo_application():
    return TodoApplicationService(unit_of_work=UnitOfWork())