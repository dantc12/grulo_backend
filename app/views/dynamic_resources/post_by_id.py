from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.posts_model import Posts
from app.sessions_ids import sessions_ids


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

    def post(self, post_id):  # add a comment
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        parser.add_argument('text', required=True)
        args = parser.parse_args()

        try:
            p = Posts.objects.get(post_id=post_id)
        except DoesNotExist:
            return {"message": "Post doesn't exist."}, 500
        else:
            comment_index = len(p.comments)
            p.comments += [{
                "comment_index": comment_index,
                "user_name": sessions_ids[args['session_id']],
                "text": args['text'],
                "liked_users_names": []
            }]
            response = {"message": "Added comment to post successfully."}
            response.update(p.comments[-1])
            return response, 200
