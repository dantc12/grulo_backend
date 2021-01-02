from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.models.users_model import Users


class PostById(Resource):
    def get(self, post_id):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            p = Posts.objects.get(post_id=post_id)
        except DoesNotExist:
            return {"message": "Post doesn't exist."}, 500
        else:
            response = {"message": "Found post successfully."}
            response.update(p.json())
            return response, 200


class GroupById(Resource):
    def get(self, groupid):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            g = Groups.objects.get(groupid=groupid)
        except DoesNotExist:
            return {"message": "Group doesn't exist."}, 500
        else:
            response = {"message": "Found group successfully."}
            response.update(g.json())
            return response, 200


class UserByName(Resource):
    def get(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            u = Users.objects.get(groupid=username)
        except DoesNotExist:
            return {"message": "User doesn't exist."}, 500
        else:
            response = {"message": "Found user successfully."}
            response.update(u.json())
            return response, 200
