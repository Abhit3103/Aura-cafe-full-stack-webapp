from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from schemas import OrderCreate

@router.post("")
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@router.get("")
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)