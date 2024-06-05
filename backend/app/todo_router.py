from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from datetime import date
from fastapi import Response

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_or_update_todo(db: Session, todo_data: schemas.TodoCreate, todo_id: int = None):
    if todo_id:
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db_todo = models.Todo()
        db_todo.number = db.query(models.Todo).count() + 1
        db_todo.added_date = date.today()
        db_todo.due_date = todo_data.due_date
        db_todo.task_name = todo_data.task_name
        db_todo.priority = todo_data.priority  # 直接代入
        db.add(db_todo)
    try:
        db.commit()
        db.refresh(db_todo)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    return db_todo

@router.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    print("Received todo data:", todo.model_dump())  # デバッグ用のログを追加
    return create_or_update_todo(db, todo)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    print(db.query(models.Todo).all())
    return db.query(models.Todo).all()

@router.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo

@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return create_or_update_todo(db, todo, todo_id)

@router.options("/todos/")
def options_todos():
    return Response(status_code=204)