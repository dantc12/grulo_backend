from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.utils import get_google_maps_coors


class GetPostsByCoor(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        locs = get_google_maps_coors(args.get('coordinates'))

        res_posts = []
        for loc in locs:
            try:
                group = Groups.objects.get(groupid=loc.get("place_id"))
            except DoesNotExist:
                raise Exception("Issue with getting google group from grulo groups db.")

            group_posts = [Posts.objects.get(post_id=post_id) for post_id in group.post_ids]
            res_posts += group_posts

        return {
            "message": "retrieved posts successfuly.",
            "posts": res_posts
        }, 200
