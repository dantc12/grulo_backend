import datetime
from mongoengine import Document
from mongoengine import (
    DateTimeField,
    StringField,
    EmailField,
    ListField,
)


class Users(Document):
    username = StringField(max_length=60, required=True, unique=True)
    email = EmailField(unique=True)
    password = StringField(max_length=60, required=True)
    address = StringField(max_length=60, required=True)
    firstname = StringField(max_length=20)
    lastname = StringField(max_length=20)
    birthday = DateTimeField(default=datetime.datetime.utcnow)
    phone = StringField(max_length=20)
    gender = StringField(max_length=20)
    bio = StringField(max_length=100)
    group_ids = ListField(default=[])
    post_ids = ListField(default=[])

    def json(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthday": str(self.birthday),
            "phone": self.phone,
            "gender": self.gender,
            "bio": self.bio,
            "group_ids": self.group_ids,
            "post_ids": self.post_ids
        }
        return user_dict

    def __str__(self):
        return str(self.json())
