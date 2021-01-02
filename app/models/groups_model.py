import datetime
from mongoengine import Document
from mongoengine import (
    #DateTimeField,
    StringField,
    #EmailField,
    # ReferenceField,
    # ListField,
    # FileField,
    # ImageField,
)

class Groups(Document):
    groupname = StringField(max_length=60, required=True)
    grouptype = StringField(max_length=60, required=True)

    def json(self):
        group_dict = {
            "groupname": self.groupname,
            "grouptype": self.grouptype
        }

        return group_dict

    def __str__(self):
        return str(self.json())