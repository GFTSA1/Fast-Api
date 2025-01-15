from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from .. import models, schemas, oath2
from starlette.responses import Response
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=["like"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def get_likes(like: schemas.Like, db: Session = Depends(get_db), current_user = Depends(oath2.get_current_user_id)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if like.direction == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already liked this post.")
        new_like = models.Like(post_id = like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully liked this post."}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist.")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully unliked this post."}

