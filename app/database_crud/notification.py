import datetime
import uuid
from enum import Enum

from bson import ObjectId
from mongoengine import (
    DateTimeField,
    ObjectIdField,
    BooleanField, EnumField
)
from mongoengine import EmbeddedDocument, IntField


class NotificationType(Enum):
    FriendRequest = "FriendRequestNotification"
    NewGroupPosts = "NewGroupPosts"
    NewCommentsOnPost = "NewCommentsOnPost"
    NewLikesOnPost = "NewLikesOnPost"


class Notification(EmbeddedDocument):
    id = ObjectIdField(default=ObjectId())
    seen = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    type = EnumField(NotificationType, required=True)

    meta = {
        "allow_inheritance": True
    }


class UserNotification(Notification):  # A notification originating from some specific user
    user = ObjectIdField(required=True)


class GroupCountNotification(Notification):  # A notification originating from a specific group, aggregating to a count
    count = IntField(default=1)
    group = ObjectIdField(required=True)


class PostCountNotification(Notification):  # A notification originating from a specific post, aggregating to a count
    count = IntField(default=1)
    post = ObjectIdField(required=True)
