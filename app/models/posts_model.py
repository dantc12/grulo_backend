import datetime
from mongoengine import Document
from mongoengine import (
    DateTimeField,
    StringField,
    IntField,
    ListField
    # ReferenceField,
    # ListField,
    # FileField,
    # ImageField,
)


class Posts(Document):
    post_id = IntField(required=True, unique=True)
    user_name = StringField(max_length=60, required=True)
    group_name = StringField(max_length=60, required=True)
    text = StringField(max_length=60, required=True)
    post_date = DateTimeField(default=datetime.datetime.utcnow)
    last_update = DateTimeField(default=datetime.datetime.utcnow)
    comments = ListField(default=[])

    def json(self):
        return {
            "post_id": self.post_id,
            "user_name": self.user_name,
            "group_name": self.group_name,
            "text": self.text,
            "post_date": str(self.post_date),
            "last_update": str(self.last_update),
            "comments": self.comments
        }

    def __str__(self):
        return str(self.json())
