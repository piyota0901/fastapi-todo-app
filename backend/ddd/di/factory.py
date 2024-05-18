import os

from dotenv import load_dotenv
from fastapi import Depends

from backend.ddd.application.todo_application import TodoApplicationService
from backend.ddd.infrastructure.repositories.transaction import (
    FakeUnitOfWork,
    IUnitOfWork,
    UnitOfWork,
)

load_dotenv()

environment = os.getenv("ENVIRONMENT")

def get_unit_of_work() -> IUnitOfWork:
    if environment == "DEVELOPMENT":
        return FakeUnitOfWork()
    elif environment == "STAGING":
        return UnitOfWork()
    elif environment == "PRODUCTION":
        return UnitOfWork()
    else:
        raise ValueError("Invalid environment")

def get_todo_application(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)):
    return TodoApplicationService(unit_of_work=unit_of_work)