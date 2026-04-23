from sqlalchemy.orm import Session
from fastapi import HTTPException
import models


# =========================
# USER
# =========================

def create_user(db: Session, user, hashed_password: str):
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# =========================
# MENU
# =========================

def create_menu_item(db: Session, item):
    db_item = models.MenuItem(
        name=item.name,
        price=item.price,
        image=item.image,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_menu(db: Session):
    return db.query(models.MenuItem).all()


def get_menu_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()


def update_menu_item(db: Session, item_id: int, item_data):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item:
        db_item.name = item_data.name
        db_item.price = item_data.price
        if hasattr(item_data, 'image') and item_data.image is not None:
            db_item.image = item_data.image
        if hasattr(item_data, 'description') and item_data.description is not None:
            db_item.description = item_data.description
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_menu_item(db: Session, item_id: int):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# =========================
# ORDER
# =========================

def create_order(db: Session, order):
    total = 0

    for item in order.items:
        # Correct model name
        menu_item = db.query(models.MenuItem).filter(
            models.MenuItem.id == item.item_id
        ).first()

        # If item not found → error
        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Item {item.item_id} not found"
            )

        # Calculate total
        total += menu_item.price * item.quantity

    # Create ONE order (correct logic)
    db_order = models.Order(
        total=total,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        order_type=order.order_type,
        address=order.address,
        seat_number=order.seat_number
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


# =========================
# GET ORDERS
# =========================

def get_orders(db: Session):
    return db.query(models.Order).all()