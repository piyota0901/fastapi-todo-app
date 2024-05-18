import abc
from datetime import datetime, timezone
from uuid import uuid4

from backend.ddd.domain.entities.todo import Todo


class ITodoFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create(title: str, description: str) -> Todo:
        raise NotImplementedError()

class TodoFactory(ITodoFactory):
    @staticmethod
    def create(title: str, description: str, is_done: bool=False) -> Todo:
        """Create a new `Todo` instance.

        Args:
            title (str): The title of the todo.
            description (str): The description of the todo.
            is_done (bool, optional): The status of the todo. Defaults to False.

        Returns:
            Todo: The new `Todo` instance.
        """
        return Todo(
                    id=str(uuid4()), 
                    title=title, 
                    description=description, 
                    is_done=is_done,
                    create_at=datetime.now(tz=timezone.utc),
                    updated_at=datetime.now(tz=timezone.utc)
                )