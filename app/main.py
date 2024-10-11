# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import List
from app.models.todo_model import TodoItem  # 修正されたインポート
from app.services.todo_service import TodoService

app = FastAPI()

# 共有されるTodoServiceのインスタンスを作成
todo_service = TodoService()

# TodoServiceの依存性注入
def get_todo_service():
    return todo_service  # 毎回同じインスタンスを返す

# HTTPExceptionに対するエラーハンドラ
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 新しいタスクの作成
@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem, todo_service: TodoService = Depends(get_todo_service)) -> TodoItem:
    if not todo.task:
        raise HTTPException(status_code=422, detail="タスクは空であってはいけません。")
    if len(todo.task) > 255:
        raise HTTPException(status_code=422, detail="タスクは255文字を超えてはいけません。")

    return todo_service.create_todo_item(todo)

# すべてのタスクの取得
@app.get("/todos/", response_model=List[TodoItem])
def get_todos(todo_service: TodoService = Depends(get_todo_service)) -> List[TodoItem]:
    return todo_service.get_all_todos()

# IDに基づくタスクの取得
@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int, todo_service: TodoService = Depends(get_todo_service)) -> TodoItem:
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"指定されたタスク（ID: {todo_id}）は見つかりませんでした。")
    return todo

# IDに基づくタスクの更新
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem, todo_service: TodoService = Depends(get_todo_service)) -> TodoItem:
    todo = todo_service.update_todo_item(todo_id, updated_todo)
    if not todo:
        raise HTTPException(status_code=404, detail=f"指定されたタスク（ID: {todo_id}）は見つかりませんでした。")
    return todo

# IDに基づくタスクの削除
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, todo_service: TodoService = Depends(get_todo_service)) -> dict:
    if not todo_service.delete_todo_item(todo_id):
        raise HTTPException(status_code=404, detail=f"指定されたタスク（ID: {todo_id}）は見つかりませんでした。")
    return {"message": f"タスク（ID: {todo_id}）が正常に削除されました。"}

# すべてのタスクの削除
@app.delete("/todos/")
def delete_all_todos(todo_service: TodoService = Depends(get_todo_service)) -> dict:
    todo_service.delete_all_todos()
    return {"message": "すべてのタスクが削除されました。"}
