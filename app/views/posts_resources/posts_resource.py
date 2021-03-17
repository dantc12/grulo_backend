from typing import Dict

from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.models.users_model import Users
from app.sessions_ids import sessions_ids
from app.utils import check_if_logged_in


def create_post(body: Dict):
    session_id = body.get("session_id")
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    group_name = body.get("group_name")
    text = body.get("text")

    try:
        group = Groups.objects.get(group_name=group_name)
    except DoesNotExist:
        return {"message": "Group doesn't exist."}, 500

    #  create the post id
    post_ids = [post.post_id for post in Posts.objects]
    next_post_id = max(post_ids) + 1 if len(post_ids) > 0 else 1

    user_name = sessions_ids.get(session_id)

    post = Posts(
        post_id=next_post_id,
        user_name=user_name,
        group_name=group_name,
        text=text
    )

    post.save()
    #  add to user's posts

    user = Users.objects.get(user_name=user_name)
    user.update(post_ids=user.post_ids + [next_post_id])
    #  add to groups posts
    group.update(post_ids=group.post_ids + [next_post_id])
    return {}, 200


def get_posts_for_user(session_id: str, limit: int = None):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    user_name = sessions_ids.get(session_id)
    user = Users.objects.get(user_name=user_name)
    posts = []
    for group_id in user.group_ids:
        group = Groups.objects.get(group_id=group_id)
        posts += [Posts.objects.get(post_id=post_id) for post_id in group.post_ids]
    if len(posts) == 0:
        return {
            "posts": []
        }, 200
    else:
        if limit:
            return {
                "posts": [p.json() for p in posts[:limit]]
            }, 200
        else:
            return {
                "posts": [p.json() for p in posts]
            }, 200
