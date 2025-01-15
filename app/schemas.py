from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user: UserResponse
    class Config:
        from_attributes = True

class SimplifiedUserResponse(BaseModel):
    email: EmailStr

class PostResponseSimplified(PostBase):
    id: int
    created_at: datetime
    user: SimplifiedUserResponse
    class Config:
        from_attributes = True


class PostResponseOnUser(BaseModel):
    Post: PostResponseSimplified
    Likes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Like(BaseModel):
    post_id: int
    direction: conint(le=1)

class PostOut(BaseModel):
    Post: PostResponse
    Likes: int

    class Config:
        orm_mode = True


