import datetime
from mongoengine import Document
from mongoengine import (
    #DateTimeField,
    StringField,
    ListField,
    #EmailField,
    # ReferenceField,
    # ListField,
    # FileField,
    # ImageField,
)

class Groups(Document):
    groupname = StringField(max_length=100, required=True)
    grouptype = StringField(max_length=100, required=True)
    groupid = StringField(max_length=100, required=True)
    users = ListField(StringField(), default=["noam"], required=True)

    def json(self):
        group_dict = {
            "groupname": self.groupname,
            "grouptype": self.grouptype,
            "groupid": self.groupid,
            "users": self.users
        }

        return group_dict

    def __str__(self):
        return str(self.json())