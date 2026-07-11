"""
Posts routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from models import Post, User, Comment, Like, PostCategory
from schemas import PostCreate, PostResponse, PostDetailResponse, CommentCreate, CommentResponse
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("", response_model=List[PostResponse])
async def get_posts(
    locality_id: str = Query(...),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get posts for a locality"""
    skip = (page - 1) * per_page
    posts = db.query(Post).filter(
        Post.locality_id == locality_id,
        Post.is_active == True
    ).order_by(Post.created_at.desc()).offset(skip).limit(per_page).all()
    
    return posts

@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post(post_id: str, db: Session = Depends(get_db)):
    """Get a specific post with comments"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@router.post("", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Create a new post"""
    post = Post(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        locality_id=current_user.locality_id,
        caption=post_data.caption,
        category=PostCategory(post_data.category),
        image=post_data.image,
        video=post_data.video,
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@router.post("/{post_id}/like", response_model=PostResponse)
async def like_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Like a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()
    
    if not existing_like:
        like = Like(
            id=str(uuid.uuid4()),
            post_id=post_id,
            user_id=current_user.id
        )
        db.add(like)
        post.likes_count += 1
        db.commit()
    
    db.refresh(post)
    return post

@router.post("/{post_id}/unlike", response_model=PostResponse)
async def unlike_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Unlike a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()
    
    if like:
        db.delete(like)
        post.likes_count -= 1
        db.commit()
    
    db.refresh(post)
    return post

@router.post("/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: str,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda db: get_current_user("", db))
):
    """Add comment to a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = Comment(
        id=str(uuid.uuid4()),
        post_id=post_id,
        user_id=current_user.id,
        text=comment_data.text
    )
    
    db.add(comment)
    post.comments_count += 1
    db.commit()
    db.refresh(comment)
    
    return comment

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get comments for a post"""
    skip = (page - 1) * per_page
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.desc()).offset(skip).limit(per_page).all()
    
    return comments
