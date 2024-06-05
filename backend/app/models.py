from sqlalchemy import Column, Integer, String, Date
from datetime import date
from .database import Base

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True)  # No., 自動で番号を振る
    added_date = Column(Date, index=True, default=lambda: date.today())  # 追加日、デフォルトで今日の日付
    due_date = Column(Date, index=True)  # 期限
    task_name = Column(String(255), index=True)  # タスク名
    priority = Column(Integer, index=True)  # 優先度整数型に変更、

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # number の自動採番はAPI側で行うため、ここでは設定しない