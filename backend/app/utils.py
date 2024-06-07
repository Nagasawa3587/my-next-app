# from app.models import Todo
# from sqlalchemy.orm import Session
# from app import schemas
# from app import models
# from app.database import get_db
# from fastapi import HTTPException, Depends
# from datetime import date

# priority_mapping = {
#     "高": 0,
#     "中": 1,
#     "低": 2
# }

# reverse_priority_mapping = {
#     0: "高",
#     1: "中",
#     2: "低"
# }

# def int_to_priority(priority_int):
#     return reverse_priority_mapping[priority_int]

# def priority_to_int(priority_str):
#     return priority_mapping[priority_str]

# def create_or_update_todo(db: Session, todo_data: schemas.TodoCreate, todo_id: int = None):
#     if todo_id:
#         db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#         if db_todo is None:
#             raise HTTPException(status_code=404, detail="Todo not found")
#     else:
#         db_todo = models.Todo()
#         db_todo.number = db.query(models.Todo).count() + 1
#         db_todo.added_date = date.today()
#         db_todo.due_date = todo_data.due_date
#         db_todo.task_name = todo_data.task_name
#         db_todo.priority = priority_to_int(todo_data.priority)  # 文字列から整数に変換
#         db.add(db_todo)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo

# def read_todos(db: Session = Depends(get_db)):
#     todos = db.query(models.Todo).all()
#     for todo in todos:
#         todo.priority = int_to_priority(todo.priority)  # 整数から文字列に変換
#     return todos
