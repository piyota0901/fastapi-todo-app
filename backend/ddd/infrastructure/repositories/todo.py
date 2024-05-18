import abc
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.ddd.domain.entities.todo import Todo as TodoEntity
from backend.ddd.infrastructure.repositories.models import TodoModel


class ITodoRepository(abc.ABC):
    @abc.abstractmethod
    def find_all(self) -> list[TodoEntity]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def find_by_id(self, id: str) -> Optional[TodoEntity]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def add(self, todo: TodoEntity) -> TodoEntity:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update(self, todo: TodoEntity) -> Optional[TodoEntity]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError()


class FakeTodoRepository(ITodoRepository):
    def __init__(self):
        self.todos: List[TodoModel] = []
    
    def find_all(self) -> List[TodoEntity]:
        return [todo.to_entity() for todo in self.todos]
    
    def find_by_id(self, id: str) -> Optional[TodoEntity]:
        todo = next((todo for todo in self.todos if todo.id == id), None)
        todo_entity = todo.to_entity() if todo is not None else None
        return todo_entity
    
    def add(self, todo: TodoEntity) -> TodoEntity:
        todo_model = TodoModel.from_entity(todo)
        self.todos.append(todo_model)
        return todo
            
    def update(self, todo: TodoEntity) -> Optional[TodoEntity]:
        todo_models = [t for t in self.todos if t.id != todo.id]
        todo_model = None if len(todo_models) == 0 else todo_models[0] 
        if todo_model is None:
            return None
        
        new_todo_model = TodoModel(
                        id=todo_model.id, # ここでidを指定しないと、新しいidが生成されてしまう
                        title=todo.title,
                        description=todo.description,
                        is_done=todo.is_done,
        )
        self.todos.remove(todo_model)        
        self.todos.append(new_todo_model)
        return new_todo_model.to_entity()
    
    def delete(self, id: str) -> None:
        self.todos = [todo for todo in self.todos if todo.id != id]


class TodoRepository(ITodoRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def find_all(self) -> List[TodoEntity]:
        todo_models = self.session.query(TodoModel).all()
        todo_entities = [todo_model.to_entity() for todo_model in todo_models]
        return todo_entities
    
    def find_by_id(self, id: str) -> Optional[TodoEntity]:
        todo_models = self.session.query(TodoModel).filter(TodoModel.id == id).first()
        return todo_models.to_entity() if todo_models is not None else None
    
    def add(self, todo: TodoEntity) -> TodoEntity:
        todo_model = TodoModel.from_entity(todo)
        self.session.add(todo_model)
        return todo
        
    def update(self, todo: TodoEntity) -> Optional[TodoEntity]:
        todo_model = self.session.query(TodoModel).filter(TodoModel.id == todo.id).first()
        if todo_model is not None:
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.is_done = todo.is_done
        return todo_model.to_entity() if todo_model is not None else None
    
    def delete(self, id: str) -> None:
        todo = self.session.query(TodoModel).filter(TodoModel.id == id).first()
        if todo is not None:
            self.session.delete(todo)
        return