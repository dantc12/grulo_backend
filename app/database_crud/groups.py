from typing import List

from . import users, models
from .. import exceptions, schemas


def get_group_by_id(group_id: str) -> models.Group:
    if models.Group.objects(group_id=group_id):
        return models.Group.objects(group_id=group_id)[0]
    raise exceptions.GroupNotFound(group_id)


def get_group_by_name(group_name: str) -> models.Group:
    if models.Group.objects(group_name=group_name):
        return models.Group.objects(group_name=group_name)[0]
    raise exceptions.GroupNotFound(group_name)


def create_group(group_create: schemas.GroupCreate) -> models.Group:
    if models.Group.objects(group_name=group_create.group_name):
        return models.Group.objects(group_name=group_create.group_name)[0]
    taken_group_ids = [group.group_id for group in models.Group.objects]
    group_id = 1
    while str(group_id) in taken_group_ids:
        group_id += 1
    group_id = str(group_id)
    group = models.Group(group_id=group_id, **group_create.dict())
    group.save()
    return group


def get_all_groups() -> List[models.Group]:
    return list(models.Group.objects())


def add_user_to_group(query_group: schemas.QueryGroup, username: str) -> models.Group:
    user = users.get_user_by_name(username)
    try:
        group = get_group_by_name(query_group.group_name)
    except exceptions.GroupNotFound:
        group = create_group(schemas.GroupCreate(**query_group.dict()))
    user.update(group_ids=user.group_ids + [group.group_id])
    group.users = group.users + [user.username]
    group.save()
    return group
