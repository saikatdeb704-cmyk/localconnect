"""
Database models for LocalConnect
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    RESIDENT = "resident"
    SHOPKEEPER = "shopkeeper"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"

class PostCategory(str, enum.Enum):
    LOST_FOUND = "lost_found"
    EVENT = "event"
    BLOOD_REQUEST = "blood_request"
    EMERGENCY = "emergency"
    UPDATE = "update"
    PHOTO = "photo"
    VIDEO = "video"
    POLL = "poll"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Locality(Base):
    __tablename__ = "localities"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    pincode = Column(String, unique=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="locality")
    posts = relationship("Post", back_populates="locality")
    shops = relationship("Shop", back_populates="locality")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.RESIDENT)
    locality_id = Column(String, ForeignKey("localities.id"))
    bio = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    locality = relationship("Locality", back_populates="users")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    orders = relationship("Order", back_populates="buyer")
    shops = relationship("Shop", back_populates="owner")
    services = relationship("Service", back_populates="provider")
    notifications = relationship("Notification", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    locality_id = Column(String, ForeignKey("localities.id"))
    caption = Column(Text)
    image = Column(String, nullable=True)
    video = Column(String, nullable=True)
    category = Column(Enum(PostCategory))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="posts")
    locality = relationship("Locality", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(String, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("posts.id"))
    user_id = Column(String, ForeignKey("users.id"))
    text = Column(Text)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(String, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("posts.id"))
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("Post", back_populates="likes")

class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    locality_id = Column(String, ForeignKey("localities.id"))
    name = Column(String, index=True)
    category = Column(String)  # kirana, vegetable, meat, etc
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    phone = Column(String)
    address = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    subscription_plan = Column(String, nullable=True)  # basic, pro, premium
    subscription_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="shops")
    locality = relationship("Locality", back_populates="shops")
    products = relationship("Product", back_populates="shop", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="shop")
    reviews = relationship("Review", back_populates="shop")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    shop_id = Column(String, ForeignKey("shops.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    stock = Column(Integer, default=0)
    image = Column(String, nullable=True)
    category = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, index=True)
    buyer_id = Column(String, ForeignKey("users.id"))
    shop_id = Column(String, ForeignKey("shops.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    amount = Column(Float)
    items_count = Column(Integer)
    payment_method = Column(String)  # online, cash_on_delivery
    delivery_address = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    buyer = relationship("User", back_populates="orders")
    shop = relationship("Shop", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(String, primary_key=True, index=True)
    provider_id = Column(String, ForeignKey("users.id"))
    locality_id = Column(String, ForeignKey("localities.id"))
    category = Column(String, index=True)  # electrician, plumber, etc
    title = Column(String)
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    phone = Column(String)
    rating = Column(Float, default=0.0)
    hourly_rate = Column(Float, nullable=True)
    availability = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    provider = relationship("User", back_populates="services")
    reviews = relationship("Review", back_populates="service")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True, index=True)
    shop_id = Column(String, ForeignKey("shops.id"), nullable=True)
    service_id = Column(String, ForeignKey("services.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    rating = Column(Integer)  # 1-5
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="reviews")
    service = relationship("Service", back_populates="reviews")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    message = Column(Text)
    type = Column(String)  # order_status, new_post, etc
    related_id = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="notifications")
