from app.sessions_ids import sessions_ids
from app.models.users_model import Users
from app.models.groups_model import Groups
from mongoengine import NotUniqueError, ValidationError, DoesNotExist

from app.utils import get_google_group_by_id, check_if_logged_in


def get_group_by_id(group_id: str, session_id: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    try:
        group = Groups.objects.get(group_id=group_id)
    except DoesNotExist:
        return {"message": "Group doesn't exist."}, 500
    else:
        return group.json(), 200


def add_user_to_group(group_id: str, session_id: str):
    if session_id not in sessions_ids.keys():
        return {
                   "message": "Not logged in"
               }, 400
    user_name = sessions_ids[session_id]

    user = Users.objects.get(user_name=user_name)
    user_group_ids = user.group_ids
    user_group_ids.append(group_id)
    Users.objects(user_name=user_name).update(group_ids=user_group_ids)

    try:
        group = Groups.objects.get(group_id=group_id)
        group_user_names = group.user_names
        if user_name in group_user_names:
            return {"message": "User already in group."}, 500
        group_user_names.append(user_name)
        Groups.objects(group_id=group_id).update(user_names=group_user_names)
    except DoesNotExist:
        # If new group
        group_name, group_type = get_google_group_by_id(group_id)
        group = Groups(
            group_name=group_name,
            group_type=group_type,
            group_id=group_id,
            user_names=[user_name]
        )
        try:
            group.save()
        except ValidationError:
            return {"message": "Bad input."}, 500
        except NotUniqueError as e:
            return {"message": "Group already exists."}, 500
        else:
            return {}, 200
