from typing import List

from . import models
from .. import exceptions, schemas


def get_user_by_name(username: str) -> models.User:
    if models.User.objects(username=username):
        return models.User.objects(username=username)[0]
    raise exceptions.UserNotFound(username)


def search_users_containing(partial_username: str) -> List[models.User]:
    return list(models.User.objects(username__icontains=partial_username))


def create_user(user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db_user.save()
    return db_user
