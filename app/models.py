import datetime
import json
from mongoengine import Document
from mongoengine import (
    DateTimeField,
    StringField,
    EmailField,
    # ReferenceField,
    # ListField,
    # FileField,
    # ImageField,
)


class User(Document):
    user_name = StringField(max_length=60, required=True, unique=True)
    email = EmailField(unique=True)
    password = StringField(max_length=60, required=True)
    address = StringField(max_length=60, required=True)
    birthday = DateTimeField(default=datetime.datetime.utcnow)
    phone = StringField(max_length=20)
    gender = StringField(max_length=20)
    bio = StringField(max_length=100)

    def json(self):
        user_dict = {
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password,
            "address": self.password,
            "birthday": str(self.birthday),
            "phone": self.phone,
            "gender": self.gender,
            "bio": self.bio
        }
        return user_dict

    def __str__(self):
        return str(self.json())
