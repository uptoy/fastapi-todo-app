# app/services/todo_service.py
from typing import List, Optional
from app.models.todo_model import TodoItem  # 修正されたインポート


class TodoService:
    def __init__(self):
        self.todo_items: List[TodoItem] = []
        self.id_counter: int = 1

    def create_todo_item(self, todo: TodoItem) -> TodoItem:
        todo.id = self.id_counter
        self.todo_items.append(todo)
        self.id_counter += 1
        return todo

    def get_all_todos(self) -> List[TodoItem]:
        return self.todo_items

    def get_todo_by_id(self, todo_id: int) -> Optional[TodoItem]:
        for todo in self.todo_items:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo_item(self, todo_id: int, updated_todo: TodoItem) -> Optional[TodoItem]:
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.task = updated_todo.task
            todo.completed = updated_todo.completed
        return todo

    def delete_todo_item(self, todo_id: int) -> bool:
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self.todo_items.remove(todo)
            return True
        return False

    def delete_all_todos(self) -> None:
        self.todo_items.clear()
