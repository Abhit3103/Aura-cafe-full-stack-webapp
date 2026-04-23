from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_to_cart(db, item)


@router.get("/")
def view_cart(db: Session = Depends(get_db)):
    return crud.get_cart(db)