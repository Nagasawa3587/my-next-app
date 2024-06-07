from sqlalchemy import create_engine
from app.models import Base

def recreate_database():
    engine = create_engine("mysql+pymysql://todo_user:Motoki21@localhost/todo_app")
    Base.metadata.drop_all(bind=engine)  # 既存のテーブルを削除
    Base.metadata.create_all(bind=engine)  # 新しいテーブルを作成

if __name__ == "__main__":
    recreate_database()