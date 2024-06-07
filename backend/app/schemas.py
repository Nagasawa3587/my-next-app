from pydantic import BaseModel
from datetime import date
from typing import Optional

class TodoBase(BaseModel):
    deadline: date
    title: str
    priority: int

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    deadline: Optional[date] = None
    title: Optional[str] = None
    priority: Optional[int] = None

class Todo(TodoBase):
    id: int
    number: int
    added_date: date

    class Config:
        orm_mode = True
        from_attributes = True