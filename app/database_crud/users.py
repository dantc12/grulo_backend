from typing import List

from . import models
from .. import exceptions, schemas


def get_user_by_name(username: str) -> models.User:
    user = models.User.objects(username=username).first()
    if user is None:
        raise exceptions.UserNotFound(username)
    return user


def search_users_containing(partial_username: str) -> List[models.User]:
    return list(models.User.objects(username__icontains=partial_username))


def create_user(user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db_user.save()
    return db_user
