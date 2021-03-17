from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.utils import check_if_logged_in


def get_posts_by_group_name(session_id: str, group_name: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    try:
        group = Groups.objects.get(group_name=group_name)
    except DoesNotExist:
        return {"message": "Group doesn't exist."}, 500

    return [Posts.objects.get(post_id=post_id).json() for post_id in group.post_ids], 200
