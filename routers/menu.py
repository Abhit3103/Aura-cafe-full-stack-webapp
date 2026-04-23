from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.MenuItemResponse)
def add_menu(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db, item)


@router.get("/", response_model=list[schemas.MenuItemResponse])
def get_menu(db: Session = Depends(get_db)):
    return crud.get_menu(db)


@router.put("/{item_id}", response_model=schemas.MenuItemResponse)
def update_menu_item(item_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_menu_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return crud.update_menu_item(db, item_id, item)


@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_menu_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    crud.delete_menu_item(db, item_id)
    return {"message": "Menu item deleted successfully"}
