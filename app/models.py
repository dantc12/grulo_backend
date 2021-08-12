import datetime
from mongoengine import Document
from mongoengine import (
    DateTimeField,
    StringField,
    EmailField,
    ListField,
)


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    address = StringField()
    first_name = StringField()
    last_name = StringField()
    birthday = DateTimeField()
    phone = StringField()
    gender = StringField()
    bio = StringField()
    group_ids = ListField(StringField(), default=[])
    post_ids = ListField(StringField(), default=[])

    meta = {"collection": "users"}

    def to_dict(self):
        return self.to_mongo(use_db_field=False).to_dict()

    def __str__(self):
        return str(self.to_dict())


class Post(Document):
    post_id = StringField(required=True, unique=True)
    username = StringField(required=True)  # posting user
    group_name = StringField(required=True)  # the group being posted on
    text = StringField(required=True)
    post_date = DateTimeField(default=datetime.datetime.utcnow)
    last_update = DateTimeField(default=datetime.datetime.utcnow)

    likes = ListField(default=[])  # TODO add model for this
    comments = ListField(default=[])  # TODO add model for this

    meta = {"collection": "posts"}

    def to_dict(self):
        return self.to_mongo(use_db_field=False).to_dict()

    def __str__(self):
        return str(self.to_dict())


class Group(Document):
    group_id = StringField(required=True, unique=True)
    group_name = StringField(required=True, unique=True)
    group_type = StringField(required=True)
    users = ListField(StringField(), default=[])
    post_ids = ListField(StringField(), default=[])

    meta = {"collection": "groups"}

    def to_dict(self):
        return self.to_mongo(use_db_field=False).to_dict()

    def __str__(self):
        return str(self.to_dict())
