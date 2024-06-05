from pydantic import BaseModel
from datetime import date
from typing import Optional

class TodoBase(BaseModel):
    due_date: date
    task_name: str
    priority: int  # 優先度を整数型で扱う

class TodoCreate(TodoBase):
    # Todoの作成時には、numberとadded_dateは含めない
    pass

class TodoUpdate(BaseModel):
    due_date: Optional[date] = None
    task_name: Optional[str] = None
    priority: Optional[int] = None

class Todo(TodoBase):
    id: int  # データベースに保存されているTodoのID
    number: int  # No.
    added_date: date  # 追加日

    class Config:
        from_attributes = True
        orm_mode = True