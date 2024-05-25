import pytest

from backend.ddd.application.exceptions import TodoNotFound
from backend.ddd.application.todo_application import TodoApplicationService
from backend.ddd.infrastructure.repositories.transaction import FakeUnitOfWork
from backend.web.schemas.todo import TodoCreate as TodoCreateSchema
from backend.web.schemas.todo import TodoUpdate as TodoUpdateSchema


def test_create_valid_case():
    """TODOを作成する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    new_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.create(new_todo=new_todo)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual.title == "title"
    assert actual.description == "description"
    assert actual.is_done is False
    assert actual.create_at is not None
    assert actual.updated_at is not None


def test_create_valid_case_with_is_done_true():
    """is_doneを指定してTODOを作成する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    new_todo = TodoCreateSchema(
        title="title",
        description="description",
        is_done=True
    )
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.create(new_todo=new_todo)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual.title == "title"
    assert actual.description == "description"
    assert actual.is_done is True
    assert actual.create_at is not None
    assert actual.updated_at is not None


def test_create_valid_case_same_todo():
    """同じTODOを作成する場合のテスト
    
    同じタイトルと説明のTODOを作成した場合、idが異なることを確認する
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    new_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.create(new_todo=new_todo)
    actual2 = todo_application_service.create(new_todo=new_todo)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual != actual2


def test_get_todo_list_valid_case():
    """TODO一覧を取得する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    # 事前にTODOを複数作成してリポジトリに登録する
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    new_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    todo_application_service.create(new_todo=new_todo)
    todo_application_service.create(new_todo=new_todo)
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.get_todo_list()
    
    # ----------------------
    # Assert
    # ----------------------
    assert len(actual) == 2


def test_get_todo_by_id_valid_case():
    """TODOをIDで取得する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    # 事前にTODOを作成してリポジトリに登録する
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    new_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    created_todo = todo_application_service.create(new_todo=new_todo)
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.get_todo_by_id(todo_id=created_todo.id)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual.id == created_todo.id
    assert actual.title == created_todo.title
    assert actual.description == created_todo.description
    assert actual.is_done == created_todo.is_done
    assert actual.create_at == created_todo.create_at
    assert actual.updated_at == created_todo.updated_at


def test_get_todo_by_id_when_todo_not_found():
    """存在しないTODOをIDで取得する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    # ----------------------
    # Act & Assert
    # ----------------------
    with pytest.raises(TodoNotFound):
        todo_application_service.get_todo_by_id(todo_id="invalid_todo_id")


def test_update_todo_valid_case():
    """TODOを更新する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    # 事前にTODOを作成してリポジトリに登録する
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    pre_register_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    
    created_todo = todo_application_service.create(new_todo=pre_register_todo)
    
    # 更新用のTODOを作成する
    update_todo = TodoUpdateSchema(
        id=created_todo.id,
        title="title2",
        description="description2",
        is_done=True
    )
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.update(update_todo=update_todo)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual.id == update_todo.id
    assert actual.title == "title2"
    assert actual.description == "description2"
    assert actual.is_done is True
    assert actual.create_at == created_todo.create_at
    assert actual.updated_at > created_todo.updated_at # 更新日時が更新されていることを確認する


def test_update_todo_when_todo_not_found():
    """存在しないTODOを更新する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    update_todo = TodoUpdateSchema(
        id="invalid_todo_id",
        title="title2",
        description="description2",
        is_done=True
    )
    
    # ----------------------
    # Act & Assert
    # ----------------------
    with pytest.raises(TodoNotFound):
        todo_application_service.update(update_todo=update_todo)


def test_delete_todo_valid_case():
    """TODOを削除する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    # 事前にTODOを作成してリポジトリに登録する
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    pre_register_todo = TodoCreateSchema(
        title="title",
        description="description"
    )
    
    created_todo = todo_application_service.create(new_todo=pre_register_todo)
    
    # ----------------------
    # Act
    # ----------------------
    actual = todo_application_service.delete_by_id(todo_id=created_todo.id)
    
    # ----------------------
    # Assert
    # ----------------------
    assert actual is None
    

def test_delete_todo_when_todo_not_found():
    """存在しないTODOを削除する場合のテスト
    """
    # ----------------------
    # Arrange
    # ----------------------
    unit_of_work = FakeUnitOfWork()
    todo_application_service = TodoApplicationService(unit_of_work=unit_of_work)
    
    # ----------------------
    # Act & Assert
    # ----------------------
    with pytest.raises(TodoNotFound):
        todo_application_service.delete_by_id(todo_id="invalid_todo_id")