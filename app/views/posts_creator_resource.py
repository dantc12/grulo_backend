from flask_restful import Resource, reqparse
from mongoengine import ValidationError

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

        post_ids = [post.post_id for post in Posts.objects]
        next_post_id = max(post_ids) + 1

        session_id = args.get('session_id')
        username = sessions_ids.get(session_id)
        u = Users.objects.get(username=username)
        u.update(post_ids=u.post_ids + [next_post_id])

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
            response = {"message": "Post created successfully."}
            response.update(p.json())
            return response, 200
