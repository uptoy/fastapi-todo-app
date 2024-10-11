# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.todo_model import TodoItem  # 修正されたインポート


client = TestClient(app)

@pytest.fixture
def create_test_todo():
    """テスト用タスクの作成を行うヘルパー関数"""
    test_todo = {"id": 1, "task": "Learn FastAPI", "completed": False}
    response = client.post("/todos/", json=test_todo)
    assert response.status_code == 200  # POSTが成功したか確認
    return test_todo

@pytest.fixture
def delete_all_todos():
    """テスト前後ですべてのタスクをクリアするヘルパー関数"""
    client.delete("/todos/")
    yield
    client.delete("/todos/")

# タスクの作成テスト
def test_create_todo():
    test_todo = {"id": 1, "task": "Learn FastAPI", "completed": False}
    response = client.post("/todos/", json=test_todo)
    assert response.status_code == 200
    assert response.json() == test_todo

# タスクの取得テスト
def test_get_todos(create_test_todo):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # 少なくとも1つのタスクがあることを確認

# 特定タスクの取得テスト
def test_get_todo(create_test_todo):
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == create_test_todo

# タスクの更新テスト
def test_update_todo():
    updated_todo = {"id": 1, "task": "Learn FastAPI and deploy", "completed": True}
    post_response = client.post("/todos/", json={"id": 1, "task": "Learn FastAPI", "completed": False})
    assert post_response.status_code == 200
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 200
    assert response.json() == updated_todo

# タスクの削除テスト
def test_delete_todo():
    post_response = client.post("/todos/", json={"id": 1, "task": "Learn FastAPI", "completed": False})
    assert post_response.status_code == 200
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "タスク（ID: 1）が正常に削除されました。"}

# タスクが空の場合のテスト（バリデーションエラー）
def test_create_todo_with_empty_task():
    empty_todo = {"id": 2, "task": "", "completed": False}
    response = client.post("/todos/", json=empty_todo)
    assert response.status_code == 422
    assert response.json() == {"detail": "タスクは空であってはいけません。"}

# タスクが255文字を超える場合のテスト（バリデーションエラー）
def test_create_todo_with_long_task():
    long_task_todo = {"id": 3, "task": "A" * 256, "completed": False}
    response = client.post("/todos/", json=long_task_todo)
    assert response.status_code == 422
    assert response.json() == {"detail": "タスクは255文字を超えてはいけません。"}

# 存在しないタスクIDでの取得テスト
def test_get_non_existent_todo():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "指定されたタスク（ID: 999）は見つかりませんでした。"}

# 存在しないタスクIDでの削除テスト
def test_delete_non_existent_todo():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "指定されたタスク（ID: 999）は見つかりませんでした。"}
