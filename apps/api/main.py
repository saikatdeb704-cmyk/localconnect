from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from database import engine
from models import Base
from routes import auth, posts, shops, orders

logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting LocalConnect API")
    yield
    # Shutdown
    logger.info("Shutting down LocalConnect API")

app = FastAPI(
    title="LocalConnect API",
    description="One app for your entire locality",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(shops.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "LocalConnect API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
