from typing import List

from . import models
from .. import exceptions, schemas


def get_user_by_name(username: str) -> models.User:
    user = models.User.objects(username=username).first()
    if user is None:
        raise exceptions.UserNotFound(username)
    return user


def get_user_by_id(id: str) -> models.User:
    user = models.User.objects(id=id).first()
    if user is None:
        raise exceptions.UserNotFound(id)
    return user


def agree_share_to_user(recipient_user: models.User, sharing_user: models.User) -> models.User:
    """
    The recipient user must come from the `requesting_share_users` users.
    Meaning he requested to share information in the first place.
    :param recipient_user: the user we are sharing our information with
    :param sharing_user: the user sharing his information
    """
    if recipient_user.id not in sharing_user.shared_users and \
            recipient_user.id in sharing_user.requesting_share_users:
        sharing_user.shared_users.append(recipient_user.id)
        sharing_user.requesting_share_users.remove(recipient_user.id)
        sharing_user.save()
        recipient_user.shared_users.append(sharing_user.id)
        recipient_user.save()
    return sharing_user


def request_share_from_user(requesting_user: models.User, sharing_user: models.User) -> models.User:
    """
    :param requesting_user: the user requesting to share information
    :param sharing_user: the user being requested to share information
    """
    if requesting_user.id not in sharing_user.shared_users and \
            requesting_user.id not in sharing_user.requesting_share_users:
        sharing_user.requesting_share_users.append(requesting_user.id)
        sharing_user.save()
    return sharing_user


def search_users_containing(partial_username: str) -> List[models.User]:
    return list(models.User.objects(username__icontains=partial_username))


def create_user(user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db_user.save()
    return db_user


def edit_user(user_edits: schemas.UserEdit, user: models.User) -> models.User:
    user.update(**user_edits.dict(exclude_unset=True))
    user = models.User.objects(id=user.id).first()
    return user
