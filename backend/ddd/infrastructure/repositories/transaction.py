import abc
import copy
from types import TracebackType
from typing import Optional

from backend.ddd.infrastructure.database import session_factory
from backend.ddd.infrastructure.repositories.todo import (
    FakeTodoRepository,
    ITodoRepository,
    TodoRepository,
)


class IUnitOfWork(abc.ABC):
    
    todo_repository: ITodoRepository
    
    def __enter__(self) -> "IUnitOfWork":
        raise NotImplementedError()
    
    def __exit__(self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]):
        raise NotImplementedError()


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = session_factory
    
    def __enter__(self) -> "IUnitOfWork":
        self.__session = self.session_factory()
        self.todo_repository = TodoRepository(session=self.__session)
        return self
    
    def __exit__(self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]):
        if exc_type is not None:
            self.__session.rollback()
        else:
            self.__session.commit()
        self.__session.close()


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.todo_repository = FakeTodoRepository()
        self.__todo_original = copy.deepcopy(self.todo_repository.todos)
        pass
    
    def __enter__(self) -> "IUnitOfWork":
        return self
    
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None):
        if exc_type is not None:
            self.todo_repository.todos = self.__todo_original # type: ignore
        return None
    
    