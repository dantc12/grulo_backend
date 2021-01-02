from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.users_model import Users


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
