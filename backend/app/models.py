from sqlalchemy import Column, Integer, String, Date
from datetime import date
from .database import Base

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True)
    added_date = Column(Date, index=True, default=lambda: date.today())
    deadline = Column(Date, index=True)
    title = Column(String(255), index=True)
    priority = Column(Integer, index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
