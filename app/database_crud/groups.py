from typing import List

from . import models
from .. import exceptions, schemas


def get_group_by_name(group_name: str) -> models.Group:
    if models.Group.objects(group_name=group_name):
        return models.Group.objects(group_name=group_name)[0]
    raise exceptions.GroupNotFound(group_name)


def create_group(group_create: schemas.GroupCreate) -> models.Group:
    if models.Group.objects(group_name=group_create.group_name):
        return models.Group.objects(group_name=group_create.group_name)[0]
    group = models.Group(**group_create.dict())
    group.save()
    return group


def search_groups_containing(partial_group_name: str) -> List[models.Group]:
    return list(models.Group.objects(group_name__icontains=partial_group_name))


def get_all_groups() -> List[models.Group]:
    return list(models.Group.objects())


def add_user_to_group(query_group: schemas.QueryGroup, user: models.User) -> models.Group:
    try:
        group = get_group_by_name(query_group.group_name)
    except exceptions.GroupNotFound:
        group = create_group(schemas.GroupCreate(**query_group.dict()))
    if user.username not in group.users:
        user.update(groups=user.groups + [group.group_name])
        group.users = group.users + [user.username]
        group.save()
    return group
