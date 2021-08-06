from typing import List

from .. import exceptions, schemas, models


def get_user_by_name(username: str) -> models.User:
    if models.User.objects(username=username):
        return models.User.objects(username=username)[0]
    raise exceptions.UserNotFound(username)


def get_all_users() -> List[models.User]:
    return list(models.User.objects)


def create_user(user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db_user.save()
    return db_user
