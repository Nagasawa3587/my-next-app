from sqlalchemy.orm import Session
from app.models import Todo
from app.todo_router import get_db, read_todos

def debug_read_todos():
    db = next(get_db())  # ジェネレータからDBセッションを取得
    try:
        query = db.query(Todo.id, Todo.number, Todo.added_date, Todo.title, Todo.priority)
        todos = query.all()

        for todo in todos:
            print(f"ID: {todo.id}, Number: {todo.number}, Title: {todo.title}, Deadline: {todo.deadline}, Priority: {todo.priority}")

        return todos
    finally:
        db.close()  # セッションを適切にクローズ

if __name__ == "__main__":
    debug_read_todos()