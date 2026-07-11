"""
Shops and products routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from models import Shop, Product, User, UserRole
from schemas import ShopCreate, ShopResponse, ShopDetailResponse, ProductCreate, ProductResponse
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/shops", tags=["shops"])

@router.get("", response_model=List[ShopResponse])
async def get_shops(
    locality_id: str = Query(...),
    category: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get shops in a locality"""
    skip = (page - 1) * per_page
    query = db.query(Shop).filter(
        Shop.locality_id == locality_id,
        Shop.is_active == True
    )
    
    if category:
        query = query.filter(Shop.category == category)
    
    shops = query.order_by(Shop.created_at.desc()).offset(skip).limit(per_page).all()
    return shops

@router.get("/{shop_id}", response_model=ShopDetailResponse)
async def get_shop(shop_id: str, db: Session = Depends(get_db)):
    """Get shop details with products"""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    return shop

@router.post("", response_model=ShopResponse)
async def create_shop(
    shop_data: ShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Create a new shop (shopkeeper only)"""
    if current_user.role != UserRole.SHOPKEEPER:
        raise HTTPException(status_code=403, detail="Only shopkeepers can create shops")
    
    shop = Shop(
        id=str(uuid.uuid4()),
        owner_id=current_user.id,
        locality_id=current_user.locality_id,
        name=shop_data.name,
        category=shop_data.category,
        phone=shop_data.phone,
        address=shop_data.address,
        lat=shop_data.lat,
        lng=shop_data.lng,
        description=shop_data.description
    )
    
    db.add(shop)
    db.commit()
    db.refresh(shop)
    
    return shop

@router.post("/{shop_id}/products", response_model=ProductResponse)
async def add_product(
    shop_id: str,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Add product to shop"""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    product = Product(
        id=str(uuid.uuid4()),
        shop_id=shop_id,
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        description=product_data.description,
        category=product_data.category
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product

@router.get("/{shop_id}/products", response_model=List[ProductResponse])
async def get_products(
    shop_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get products in a shop"""
    skip = (page - 1) * per_page
    products = db.query(Product).filter(
        Product.shop_id == shop_id,
        Product.is_active == True
    ).offset(skip).limit(per_page).all()
    
    return products

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Update product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    shop = db.query(Shop).filter(Shop.id == product.shop_id).first()
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    product.name = product_data.name
    product.price = product_data.price
    product.stock = product_data.stock
    product.description = product_data.description
    product.category = product_data.category
    
    db.commit()
    db.refresh(product)
    
    return product
