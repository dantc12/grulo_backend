from app import exceptions, models


# TODO Not done here

def get_group_by_id(group_id: str) -> models.Group:
    if models.Group.objects(group_id=group_id):
        return models.Group.objects(group_id=group_id)[0]
    raise exceptions.GroupNotFound(group_id)


def get_group_by_name(group_name: str) -> models.Group:
    if models.Group.objects(group_name=group_name):
        return models.Group.objects(group_name=group_name)[0]
    raise exceptions.GroupNotFound(group_name)

# TODO continue here, work on location groups using 3rd party API
