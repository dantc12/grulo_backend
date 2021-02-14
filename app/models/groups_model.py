from mongoengine import Document
from mongoengine import (
    StringField,
    ListField,
    IntField,
)


class Groups(Document):
    group_name = StringField(max_length=100, required=True)
    group_type = StringField(max_length=100, required=True)
    group_id = IntField(max_length=100, required=True)
    users = ListField(StringField(), default=[])
    post_ids = ListField(IntField(), default=[])

    def json(self):
        group_dict = {
            "group_name": self.group_name,
            "group_type": self.group_type,
            "group_id": self.group_id,
            "users": self.users,
            "post_ids": self.post_ids
        }
        return group_dict

    def __str__(self):
        return str(self.json())
