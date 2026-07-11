"""
Pydantic schemas for API requests/responses
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class LocalityBase(BaseModel):
    name: str
    city: str
    state: str
    pincode: str
    lat: float
    lng: float

class LocalityCreate(LocalityBase):
    pass

class LocalityResponse(LocalityBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    locality_id: str
    role: str = "resident"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    avatar: Optional[str]
    bio: Optional[str]
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None

# Post Schemas
class PostBase(BaseModel):
    caption: str
    category: str
    image: Optional[str] = None
    video: Optional[str] = None

class PostCreate(PostBase):
    pass

class CommentResponse(BaseModel):
    id: str
    text: str
    likes_count: int
    user: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: str
    user_id: str
    user: UserResponse
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostDetailResponse(PostResponse):
    comments: List[CommentResponse] = []

# Comment Schemas
class CommentCreate(BaseModel):
    text: str

# Shop Schemas
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str
    shop_id: str
    image: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ShopBase(BaseModel):
    name: str
    category: str
    phone: str
    address: str
    lat: float
    lng: float
    description: Optional[str] = None

class ShopCreate(ShopBase):
    pass

class ShopResponse(ShopBase):
    id: str
    owner_id: str
    image: Optional[str]
    rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class ShopDetailResponse(ShopResponse):
    products: List[ProductResponse] = []

# Order Schemas
class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    shop_id: str
    items: List[OrderItemCreate]
    payment_method: str
    delivery_address: Optional[str] = None
    notes: Optional[str] = None

class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    price: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: str
    shop_id: str
    status: str
    amount: float
    items_count: int
    payment_method: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse] = []
    delivery_address: Optional[str]

# Service Schemas
class ServiceBase(BaseModel):
    category: str
    title: str
    phone: str
    description: Optional[str] = None
    hourly_rate: Optional[float] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: str
    provider_id: str
    rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Review Schemas
class ReviewCreate(BaseModel):
    rating: int  # 1-5
    text: str

class ReviewResponse(BaseModel):
    id: str
    rating: int
    text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

# Notification Schemas
class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
