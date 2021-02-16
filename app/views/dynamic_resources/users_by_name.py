from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.users_model import Users
from app.utils import check_if_logged_in


class UserByName(Resource):
    def get(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            u = Users.objects.get(username=username)
        except DoesNotExist:
            return {"message": "User doesn't exist."}, 500
        else:
            response = {"message": "Found user successfully."}
            response.update(u.json())
            return response, 200


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
