from mongoengine import DoesNotExist

from app.models.users_model import Users
from app.utils import check_if_logged_in


def get_user_by_name(session_id: str, user_name: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    try:
        u = Users.objects.get(user_name=user_name)
    except DoesNotExist:
        return {"message": "User doesn't exist."}, 500
    else:
        return u.json(), 200
