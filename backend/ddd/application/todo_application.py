
from backend.ddd.application.exceptions import TodoNotFound
from backend.ddd.domain.factories.todo import TodoFactory
from backend.ddd.infrastructure.repositories.transaction import IUnitOfWork
from backend.web.schemas.todo import Todo as TodoSchema
from backend.web.schemas.todo import TodoCreate as TodoCreateSchema
from backend.web.schemas.todo import TodoUpdate as TodoUpdateSchema


class TodoApplicationService:
    def __init__(
        self, 
        unit_of_work: IUnitOfWork
    ):
        self.factory = TodoFactory()
        self.unit_of_work = unit_of_work

    def create(self, new_todo: TodoCreateSchema) -> TodoSchema:
        """Create a new Todo.

        Args:
            new_todo (TodoCreate): _description_
        """
        todo_entity = self.factory.create(
                                    title=new_todo.title, 
                                    description=new_todo.description, 
                                    is_done=new_todo.is_done
                                )        
        with self.unit_of_work as uow:
            todo_entity = uow.todo_repository.add(todo=todo_entity)
        
        return TodoSchema(
            id=todo_entity.id,
            title=todo_entity.title,
            description=todo_entity.description,
            is_done=todo_entity.is_done,
            create_at=todo_entity.create_at,
            updated_at=todo_entity.updated_at
        )
    
    def get_todo_list(self) -> list[TodoSchema]:
        """Todo一覧を取得する

        Returns:
            list[Todo]: _description_
        """
        with self.unit_of_work as uow:
            todo_entities = uow.todo_repository.find_all()
        
        return [
            TodoSchema(
                id=todo_entity.id,
                title=todo_entity.title,
                description=todo_entity.description,
                is_done=todo_entity.is_done,
                create_at=todo_entity.create_at,
                updated_at=todo_entity.updated_at
            )
            for todo_entity in todo_entities
        ]
    
    def get_todo_by_id(self, todo_id: str) -> TodoSchema:
        """TodoをIDで取得する

        Args:
            todo_id (int): _description_

        Returns:
            todo: Todo
        
        Raises:
            TodoNotFound: 指定IDのTodoが見つからない場合に発生する例外
        """
        with self.unit_of_work as uow:
            todo_entity = uow.todo_repository.find_by_id(id=todo_id)
        
        if todo_entity is None: 
            raise TodoNotFound
        
        return TodoSchema(
            id=todo_entity.id,
            title=todo_entity.title,
            description=todo_entity.description,
            is_done=todo_entity.is_done,
            create_at=todo_entity.create_at,
            updated_at=todo_entity.updated_at
        )
    
    def update(self, update_todo: TodoUpdateSchema) -> TodoSchema:
        """Todoを更新する

        Args:
            update_todo (Todo): _description_

        Returns:
            Todo: Todo
        
        Raises:
            TodoNotFound: 指定IDのTodoが見つからない場合に発生する例外
        """
        # FIXME: ここで新しいTodoを作成しているのを直す
        todo_entity = self.factory.create(
                            title=update_todo.title, 
                            description=update_todo.description,
                            is_done=update_todo.is_done
                            )
        with self.unit_of_work as uow:      
            updated_todo_entity = uow.todo_repository.update(todo=todo_entity)
        
        if updated_todo_entity is None:
            raise TodoNotFound
        
        return TodoSchema(
            id=updated_todo_entity.id,
            title=updated_todo_entity.title,
            description=updated_todo_entity.description,
            is_done=updated_todo_entity.is_done,
            create_at=updated_todo_entity.create_at,
            updated_at=updated_todo_entity.updated_at
        )
    
    def delete_by_id(self, todo_id: str):
        """TodoをIDで削除する

        Args:
            todo_id (int): _description_

        Raises:
            TodoNotFound: 指定IDのTodoが見つからない場合に発生する例外
            Exception: 例外
        """
        with self.unit_of_work as uow:
            todo_model = uow.todo_repository.find_by_id(id=todo_id)
        
        if todo_model is None:
            raise TodoNotFound
        
        with self.unit_of_work as uow:
            uow.todo_repository.delete(id=todo_id)
        
        return None