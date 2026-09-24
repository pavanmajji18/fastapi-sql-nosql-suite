from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from fastapi import HTTPException, status
from decimal import Decimal
from app import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_product(db: Session, product: schemas.ProductCreate):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id).all()

def update_product_inventory(db: Session, product_id: int, new_stock: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock_quantity = new_stock
    db.commit()
    db.refresh(product)
    return product

def create_order(db: Session, order_in: schemas.OrderCreate):
    user = db.query(models.User).filter(models.User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    order = models.Order(user_id=user.id, total_amount=Decimal("0.00"), status="PENDING")
    db.add(order)
    db.flush()  # generates order.id

    running_total = Decimal("0.00")

    for item in order_in.items:
        # Lock row for atomic inventory update
        product = db.query(models.Product).with_for_update().filter(models.Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

        if product.stock_quantity < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient inventory for '{product.name}'. Available: {product.stock_quantity}, Requested: {item.quantity}"
            )

        unit_price = Decimal(str(product.price))
        item_total = unit_price * Decimal(item.quantity)
        running_total += item_total

        # Deduct inventory
        product.stock_quantity -= item.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=unit_price,
            item_total=item_total
        )
        db.add(order_item)

    order.total_amount = running_total
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(desc(models.Order.created_at)).all()

def cancel_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Order is already cancelled")

    # Restore inventory
    for item in order.items:
        prod = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if prod:
            prod.stock_quantity += item.quantity

    order.status = "CANCELLED"
    db.commit()
    db.refresh(order)
    return order

# Advanced SQL operation showcasing: JOIN, WHERE, GROUP BY, ORDER BY, and Aggregates
def get_user_spending_analytics(db: Session):
    """
    SQL Equivalent:
    SELECT 
        u.id AS user_id, 
        u.name AS user_name, 
        COUNT(o.id) AS total_orders, 
        COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.status != 'CANCELLED'
    GROUP BY u.id, u.name
    ORDER BY total_spent DESC;
    """
    query = (
        db.query(
            models.User.id.label("user_id"),
            models.User.name.label("user_name"),
            func.count(models.Order.id).label("total_orders"),
            func.coalesce(func.sum(models.Order.total_amount), 0).label("total_spent")
        )
        .join(models.Order, models.User.id == models.Order.user_id)
        .filter(models.Order.status != "CANCELLED")
        .group_by(models.User.id, models.User.name)
        .order_by(desc("total_spent"))
        .all()
    )

    return [
        {
            "user_id": row.user_id,
            "user_name": row.user_name,
            "total_orders": row.total_orders,
            "total_spent": row.total_spent
        }
        for row in query
    ]