from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.models.posts_model import Posts
from app.utils import get_google_groups_by_coor, check_if_logged_in


def get_posts_by_coor(session_id: str, coordinates: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    locs = get_google_groups_by_coor(coordinates)

    res_posts = []
    for loc in locs:
        try:
            group = Groups.objects.get(group_id=loc.get("place_id"))
        except DoesNotExist:
            return {"message": "Issue with getting google group from grulo groups db."}, 401

        group_posts = [Posts.objects.get(post_id=post_id) for post_id in group.post_ids]
        res_posts += group_posts

    return res_posts, 200
