import datetime
from mongoengine import Document
from mongoengine import (
    DateTimeField,
    StringField,
    EmailField,
    ListField,
    ObjectIdField
)


class User(Document):
    username = StringField(unique=True, required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    address = StringField()
    first_name = StringField()
    last_name = StringField()
    birthday = DateTimeField()
    phone = StringField()
    gender = StringField()
    bio = StringField()
    groups = ListField(ObjectIdField(), default=[])
    posts = ListField(ObjectIdField(), default=[])

    meta = {"collection": "users"}

    def to_dict(self) -> dict:
        return self.to_mongo().to_dict()

    def __str__(self):
        return str(self.to_dict())


class Post(Document):
    user = ObjectIdField(required=True)  # posting user
    group = ObjectIdField(required=True)  # the group being posted on
    text = StringField(required=True)
    post_date = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)

    likes = ListField(default=[])
    comments = ListField(default=[])

    meta = {"collection": "posts"}

    def to_dict(self) -> dict:
        return self.to_mongo().to_dict()

    def __str__(self):
        return str(self.to_dict())


class Group(Document):
    group_name = StringField(unique=True, required=True)
    group_type = StringField(required=True)
    users = ListField(ObjectIdField(), default=[])
    posts = ListField(ObjectIdField(), default=[])

    meta = {"collection": "groups"}

    def to_dict(self) -> dict:
        return self.to_mongo().to_dict()

    def __str__(self):
        return str(self.to_dict())
