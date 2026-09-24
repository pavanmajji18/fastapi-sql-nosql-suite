from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import engine, Base, get_db
from app import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="Mini E-Commerce backend powered by FastAPI and Neon PostgreSQL",
    version="1.0.0"
)

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products", response_model=List[schemas.ProductResponse], tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)

@app.patch("/products/{product_id}/inventory", response_model=schemas.ProductResponse, tags=["Products"])
def update_product_inventory(product_id: int, payload: schemas.ProductUpdateStock, db: Session = Depends(get_db)):
    return crud.update_product_inventory(db=db, product_id=product_id, new_stock=payload.stock_quantity)

@app.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order_in=order)

@app.get("/users/{user_id}/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
def list_user_orders(user_id: int, db: Session = Depends(get_db)):
    return crud.get_orders_by_user(db=db, user_id=user_id)

@app.post("/orders/{order_id}/cancel", response_model=schemas.OrderResponse, tags=["Orders"])
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    return crud.cancel_order(db=db, order_id=order_id)

@app.get("/analytics/spending-by-user", response_model=List[schemas.UserSpendingSummary], tags=["Analytics"])
def user_spending_report(db: Session = Depends(get_db)):
    """Demonstrates SQL JOIN, WHERE, GROUP BY, ORDER BY, and SUM/COUNT aggregates."""
    return crud.get_user_spending_analytics(db=db)