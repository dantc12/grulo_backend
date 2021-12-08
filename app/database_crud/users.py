from typing import List

from . import models
from .notification import UserNotification, NotificationType
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


def respond_to_share_request(recipient_user: models.User, sharing_user: models.User, accept: bool) -> models.User:
    """
    The recipient user must come from the `requesting_share_users` users.
    Meaning he requested to share information in the first place, and we are responding to that.
    :param recipient_user: the user we are sharing our information with
    :param sharing_user: the user sharing his information
    :param accept: says if we want to accept the request or not
    """
    if recipient_user.id not in sharing_user.shared_users and \
            recipient_user.id in sharing_user.requesting_share_users:
        if accept:
            sharing_user.shared_users.append(recipient_user.id)
            sharing_user.requesting_share_users.remove(recipient_user.id)
            sharing_user.save()
            recipient_user.shared_users.append(sharing_user.id)
            recipient_user.save()
        else:
            sharing_user.requesting_share_users.remove(recipient_user.id)
            sharing_user.save()
    return sharing_user


def unshare_information_with_user(recipient_user: models.User, sharing_user: models.User) -> models.User:
    """
    The recipient should currently be sharing information with us, and we want to undo that.
    :param recipient_user: the user we are sharing our information with
    :param sharing_user: the user sharing his information
    """
    if recipient_user.id in sharing_user.shared_users and sharing_user.id in recipient_user.shared_users:
        sharing_user.shared_users.remove(recipient_user.id)
        sharing_user.save()
        recipient_user.shared_users.remove(sharing_user.id)
        recipient_user.save()
    return sharing_user


def request_share_from_user(requesting_user: models.User, sharing_user: models.User, undo: bool) -> models.User:
    """
    The requesting_user is requesting to share with sharing_user.
    :param requesting_user: the user requesting to share information
    :param sharing_user: the user being requested to share information
    :param undo: says if we want to undo an existing request
    """
    if requesting_user.id not in sharing_user.shared_users:
        if not undo:
            if requesting_user.id not in sharing_user.requesting_share_users:
                sharing_user.requesting_share_users.append(requesting_user.id)
                notification = UserNotification(type=NotificationType.FriendRequest,
                                                user=requesting_user.id)
                sharing_user.notifications[str(notification.id)] = notification
                sharing_user.save()
        else:
            if requesting_user.id in sharing_user.requesting_share_users:
                sharing_user.requesting_share_users.remove(requesting_user.id)
                sharing_user.save()
    return sharing_user


def mark_notification_as_seen(notification_id: str, user: models.User, undo: bool) -> models.User:
    if notification_id in user.notifications:
        if not undo:
            user.notifications[notification_id].seen = True
        else:
            user.notifications[notification_id].seen = False
        user.save()
    return user


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
