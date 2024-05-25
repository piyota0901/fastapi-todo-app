import pytest
from fastapi.testclient import TestClient

from backend.ddd.application.todo_application import TodoApplicationService
from backend.ddd.di.factory import get_todo_application
from backend.ddd.infrastructure.repositories.transaction import FakeUnitOfWork
from backend.web.main import app


# -----------------------------
# データベースのテスト
# app.dependency_overridesを使って、テスト用のデータベースを使用する
# https://fastapi.tiangolo.com/advanced/testing-database/
# -----------------------------
@pytest.fixture
def test_client():
    """テスト用のデータベースを使用するTestClientを返す
    
    テスト関数ごとにリポジトリを初期化する
    
    reference: https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/d3f074
    """
    unit_of_work = FakeUnitOfWork()
    def get_fake_todo_applicaiton():
        """テスト用のデータベースを使用するTodoApplicationServiceを返す
        """
        return TodoApplicationService(unit_of_work=unit_of_work)
    
    # テスト用リポジトリに差し替え
    app.dependency_overrides[get_todo_application]=get_fake_todo_applicaiton
    with TestClient(app) as client:
        yield client
    

def test_get_todos_valid_case_when_no_data(test_client: TestClient):    
    # ----------------------
    # Act
    # ----------------------
    response = test_client.get("/todo")
    
    # ----------------------
    # Assert
    # ----------------------
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo_valid_case(test_client: TestClient):
    # ----------------------
    # Act
    # ----------------------
    response = test_client.post(
        "/todo",
        json={"title": "title", "description": "description"}
    )
    # ----------------------
    # Assert
    # ----------------------
    data = response.json()

    # キャメルケースに変換されていることも確認
    assert response.status_code == 200
    assert data["title"] == "title"
    assert data["description"] == "description"
    assert data["isDone"] is False
    assert data["createAt"] is not None
    assert data["updatedAt"] is not None

def test_get_todo_valid_case(test_client: TestClient):
    # ----------------------
    # Arrange
    # ----------------------
    response = test_client.post(
        "/todo",
        json={"title": "title", "description": "description"}
    )
    todo_id = response.json()["id"]
    
    # ----------------------
    # Act
    # ----------------------
    response = test_client.get(f"/todo/{todo_id}")    
    
    # ----------------------
    # Assert
    # ----------------------
    data = response.json()
    
    assert response.status_code == 200
    assert data["id"] == todo_id
    assert data["title"] == "title"
    assert data["description"] == "description"
    assert data["isDone"] is False
    assert data["createAt"] is not None
    assert data["updatedAt"] is not None

def test_get_todo_invalid_case_when_todo_not_found(test_client: TestClient):
    # ----------------------
    # Act
    # ----------------------
    response = test_client.get("/todo/invalid_id")
    assert response.status_code == 404

def test_update_todo_valid_case(test_client: TestClient):
    # ----------------------
    # Arrange
    # ----------------------
    response = test_client.post(
        "/todo",
        json={"title": "title", "description": "description"}
    )
    todo_id = response.json()["id"]
    
    # ----------------------
    # Act
    # ----------------------
    response = test_client.patch(
        f"/todo/{todo_id}",
        json={
                "title": "updated_title", 
                "description": "updated_description",
                "isDone": True
            }
    )
    
    # ----------------------
    # Assert
    # ----------------------
    data = response.json()
    
    assert response.status_code == 200
    assert data["id"] == todo_id
    assert data["title"] == "updated_title"
    assert data["description"] == "updated_description"
    assert data["isDone"] is True
    assert data["createAt"] is not None
    assert data["updatedAt"] is not None

def test_update_todo_invalid_when_todo_not_found(test_client: TestClient):
    # ----------------------
    # Act
    # ----------------------
    response = test_client.patch(
        "/todo/invalid_id",
        json={
                "title": "updated_title", 
                "description": "updated_description",
                "isDone": True
            }
    )
    assert response.status_code == 404


def test_delete_todo_valid_case(test_client: TestClient):
    # ----------------------
    # Arrange
    # ----------------------
    response = test_client.post(
        "/todo",
        json={"title": "title", "description": "description"}
    )
    todo_id = response.json()["id"]
    
    # ----------------------
    # Act
    # ----------------------
    response = test_client.delete(f"/todo/{todo_id}")
    
    # ----------------------
    # Assert
    # ----------------------
    assert response.status_code == 204

def test_delete_todo_invalid_case_when_todo_not_found(test_client: TestClient):
    # ----------------------
    # Act
    # ----------------------
    response = test_client.delete("/todo/invalid_id")
    assert response.status_code == 404