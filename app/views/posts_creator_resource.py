from flask_restful import Resource, reqparse
from mongoengine import ValidationError, DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.models.users_model import Users
from app.sessions_ids import sessions_ids


class PostCreator(Resource):
    def post(self):  # create new post
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        parser.add_argument('groupname', required=True)
        parser.add_argument('text', required=True)
        args = parser.parse_args()

        try:
            g = Groups.objects.get(groupname=args['groupname'])
        except DoesNotExist:
            return {"message": "Group doesn't exist."}, 500

        #  create the post id
        post_ids = [post.post_id for post in Posts.objects]
        next_post_id = max(post_ids) + 1 if len(post_ids) > 0 else 1

        p = Posts(
            post_id=next_post_id,
            user_name=sessions_ids.get(args.get('session_id')),
            group_name=args.get('groupname'),
            text=args.get('text')
        )

        try:
            p.save()
        except ValidationError:
            return {"message": "Bad input."}, 500
        else:
            #  add to user's posts
            session_id = args.get('session_id')
            username = sessions_ids.get(session_id)
            u = Users.objects.get(username=username)
            u.update(post_ids=u.post_ids + [next_post_id])
            #  add to groups posts
            g.update(postids=g.postids + [next_post_id])
            response = {"message": "Post created successfully."}
            response.update(p.json())
            return response, 200
