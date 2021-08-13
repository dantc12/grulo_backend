import datetime
from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: str

    address: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[datetime.datetime]
    phone: Optional[str]
    gender: Optional[str]
    bio: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    group_ids: List[str]
    post_ids: List[str]

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    username: str


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    pass


class CommentBase(BaseModel):
    username: str
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    index: int
    likes: List[Like]


class PostBase(BaseModel):
    username: str
    group_name: str
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    post_id: str
    post_date: datetime.datetime
    last_update: datetime.datetime
    comments: List[Comment]
    likes: List[Like]

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    group_name: str
    group_type: str


class GroupCreate(GroupBase):
    pass


class QueryGroup(GroupBase):
    pass


class Group(GroupBase):
    group_id: str
    users: List[str]
    post_ids: List[str]

    class Config:
        orm_mode = True
