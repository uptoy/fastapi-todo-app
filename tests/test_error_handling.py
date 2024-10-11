# tests/test_error_handling.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 存在しないタスクの更新テスト
def test_update_non_existent_todo():
    non_existent_todo = {"id": 999, "task": "Non-existent task", "completed": False}
    response = client.put("/todos/999", json=non_existent_todo)
    assert response.status_code == 404
    assert response.json() == {"detail": "指定されたタスク（ID: 999）は見つかりませんでした。"}

# すべてのタスクを削除後、空のリストからタスクを削除しようとするテスト
def test_delete_todo_from_empty_list():
    # すべてのタスクを削除
    client.delete("/todos/")
    # 存在しないタスクを削除しようとする
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "指定されたタスク（ID: 1）は見つかりませんでした。"}
