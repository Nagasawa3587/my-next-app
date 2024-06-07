from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from datetime import date, datetime
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

    # Convert the deadline to a date object if it's a string
    if isinstance(todo_data.deadline, str):
        todo_data.deadline = datetime.strptime(todo_data.deadline, "%Y-%m-%d").date()

    db_todo.deadline = todo_data.deadline
    db_todo.title = todo_data.title
    db_todo.priority = todo_data.priority

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
    print("Received todo data:", todo)
    return create_or_update_todo(db, todo)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, title: str = None, priority: int = None):
    query = db.query(models.Todo.id, models.Todo.number, models.Todo.added_date, models.Todo.deadline, models.Todo.title, models.Todo.priority)
    if title:
        query = query.filter(models.Todo.title.contains(title))
    if priority is not None:
        query = query.filter(models.Todo.priority == priority)
    todos = query.offset(offset).limit(limit).all()
    return todos

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