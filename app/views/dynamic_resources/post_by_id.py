from typing import Dict

from mongoengine import DoesNotExist

from app.models.posts_model import Posts
from app.sessions_ids import sessions_ids
from app.utils import check_if_logged_in


def add_comment_to_post(post_id: int, body: Dict):
    session_id = body.get("session_id")
    text = body.get("text")

    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    try:
        post = Posts.objects.get(post_id=post_id)
    except DoesNotExist:
        return {"message": "Post doesn't exist."}, 500
    else:
        comment_index = len(post.comments)
        post.comments.append({
            "comment_index": comment_index,
            "user_name": sessions_ids[session_id],
            "text": text,
            "liked_users": []
        })
        post.save()
        return post.comments[-1], 200


def get_post_by_id(post_id: int, session_id: str):
    if session_id not in sessions_ids.keys():
        return {
                   "message": "Not logged in"
               }, 400

    try:
        p = Posts.objects.get(post_id=post_id)
    except DoesNotExist:
        return {"message": "Post doesn't exist."}, 500
    else:
        return p.json(), 200
