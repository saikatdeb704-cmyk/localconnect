"""
Orders routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from models import Order, OrderItem, Product, User, OrderStatus
from schemas import OrderCreate, OrderResponse, OrderDetailResponse
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Create a new order"""
    total_amount = 0
    total_items = 0
    
    # Validate and calculate total
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        
        total_amount += product.price * item.quantity
        total_items += item.quantity
    
    # Create order
    order = Order(
        id=str(uuid.uuid4()),
        buyer_id=current_user.id,
        shop_id=order_data.shop_id,
        status=OrderStatus.PENDING,
        amount=total_amount,
        items_count=total_items,
        payment_method=order_data.payment_method,
        delivery_address=order_data.delivery_address,
        notes=order_data.notes
    )
    
    # Create order items and update stock
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        order_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        
        product.stock -= item.quantity
        db.add(order_item)
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Get order details"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return order

@router.get("", response_model=List[OrderResponse])
async def get_user_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Get user's orders"""
    skip = (page - 1) * per_page
    orders = db.query(Order).filter(
        Order.buyer_id == current_user.id
    ).order_by(Order.created_at.desc()).offset(skip).limit(per_page).all()
    
    return orders

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Update order status (shop owner only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify user is shop owner
    shop = db.query(Shop).filter(Shop.id == order.shop_id).first()
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        order.status = OrderStatus(status)
        db.commit()
        db.refresh(order)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    return order

@router.delete("/{order_id}")
async def cancel_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Cancel an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only cancel pending orders")
    
    # Restore stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity
    
    order.status = OrderStatus.CANCELLED
    db.commit()
    
    return {"message": "Order cancelled"}

# Import Shop model
from models import Shop
