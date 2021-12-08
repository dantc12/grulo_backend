from datetime import datetime
from typing import Optional, List, Union, Dict

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, EmailStr, Field, BaseConfig

from .database_crud.notification import NotificationType


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class BaseMongoModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }


class Token(BaseModel):
    access_token: str
    token_type: str


# ------------------ USERS ------------------

class UserBase(BaseMongoModel):
    username: str
    email: EmailStr

    address: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[datetime]
    phone: Optional[str]
    gender: Optional[str]
    bio: Optional[str]


class UserCreate(UserBase):
    password: str


class UserEdit(UserCreate):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class NotificationBase(BaseMongoModel):
    id: OID = Field()
    seen: bool
    created: datetime
    type: NotificationType


class UserNotification(NotificationBase):
    user: OID = Field()


class GroupCountNotification(NotificationBase):
    count: int
    Group: OID = Field()


class PostCountNotification(NotificationBase):
    count: int
    post: OID = Field()


Notifications = Union[UserNotification,
                      GroupCountNotification,
                      PostCountNotification]


class User(UserBase):
    id: OID = Field()
    groups: List[OID]
    posts: List[OID]
    likes_counter: int
    notifications: Dict[str, Notifications]
    shared_users: List[OID]
    requesting_share_users: List[OID]


# ------------------ POSTS ------------------

Like = OID


class CommentBase(BaseMongoModel):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    user: OID = Field()
    index: int
    likes: List[Like]


class PostBase(BaseMongoModel):
    group: OID = Field()
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: OID = Field()
    user: OID = Field()
    post_date: datetime
    last_update: datetime
    comments: List[Comment]
    likes: List[Like]


# ------------------ GROUPS ------------------

class GroupBase(BaseMongoModel):
    group_name: str
    group_type: str


class GroupCreate(GroupBase):
    pass


class QueriedGroup(GroupBase):
    pass


class Group(GroupBase):
    id: OID = Field()
    users: List[OID]
    posts: List[OID]
