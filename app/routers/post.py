from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional

from .. import models, schemas, oath2
from starlette.responses import Response
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..schemas import UserBase, PostOut

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    posts_likes = (
        db.query(
            models.Post,
            func.count(models.Like.post_id).label("likes")
        )
        .join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
        .all()

    )
    result_posts = [{"Post": post, "Likes": likes} for post, likes in posts_likes]
    return result_posts

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponseOnUser])
async def get_post_for_user(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no such user")
    posts_likes = (
        db.query(
            models.Post,
            func.count(models.Like.post_id).label("likes")
        )
        .join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.user_id == user_id)
        .all()
    )
    results = [{"Post": post, "Likes": likes} for post, likes in posts_likes]
    return results

@router.post("", response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id)):
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id)):
    post_likes = (
        db.query(
            models.Post,
            func.count(models.Like.post_id).label("Likes")
        )
        .join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post_likes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post_likes

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: UserBase = Depends(oath2.get_current_user_id)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()