from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.posts_model import Posts


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
