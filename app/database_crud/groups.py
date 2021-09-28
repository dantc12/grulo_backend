from typing import List

from . import models
from .. import exceptions, schemas


def get_group_by_name(group_name: str) -> models.Group:
    group = models.Group.objects(group_name=group_name).first()
    if group is None:
        raise exceptions.GroupNotFound(group_name)
    return group


def get_group_by_id(id: str) -> models.Group:
    group = models.Group.objects(id=id).first()
    if group is None:
        raise exceptions.GroupNotFound(id)
    return group


def create_group(group_create: schemas.GroupCreate) -> models.Group:
    if models.Group.objects(group_name=group_create.group_name).first() is not None:
        raise exceptions.GroupAlreadyExists(group_create.group_name)
    group = models.Group(**group_create.dict())
    group.save()
    return group


def search_groups_containing(partial_group_name: str) -> List[models.Group]:
    return list(models.Group.objects(group_name__icontains=partial_group_name))


def get_all_groups() -> List[models.Group]:
    return list(models.Group.objects())


def save_queried_groups(queried_groups: List[schemas.QueriedGroup]) -> None:
    for group in queried_groups:
        models.QueriedGroup(**group.dict()).save()


def check_exists_queried_group_by_name(group_name: str) -> bool:
    group = models.QueriedGroup.objects(group_name=group_name).first()
    return group is not None


def add_user_to_group(query_group: schemas.QueriedGroup, user: models.User) -> models.Group:
    try:
        group = get_group_by_name(query_group.group_name)
    except exceptions.GroupNotFound:
        if check_exists_queried_group_by_name(query_group.group_name):
            group = create_group(schemas.GroupCreate(**query_group.dict()))
        else:
            raise exceptions.QueriedGroupNotFound(query_group.group_name)
    if user.id not in group.users:
        user.update(groups=user.groups + [group.id])
        group.users = group.users + [user.id]
        group.save()
    return group
