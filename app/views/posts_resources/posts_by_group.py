from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts


class PostsByGroupName(Resource):
    def get(self):  # get all posts given a groupname
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        parser.add_argument('groupname', required=True)
        args = parser.parse_args()

        try:
            g = Groups.objects.get(groupname=args['groupname'])
        except DoesNotExist:
            return {"message": "Group doesn't exist."}, 530

        return {
            "message": "retrieved posts of group {}".format(g.groupname),
            "posts": [Posts.objects.get(post_id=post_id) for post_id in g.postids]
        }, 200
