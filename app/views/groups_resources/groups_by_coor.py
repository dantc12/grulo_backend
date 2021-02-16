from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.sessions_ids import sessions_ids
from app.utils import get_google_groups_by_coor, check_if_logged_in


def get_groups_by_coor(session_id: str, coordinates: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    try:
        locs = get_google_groups_by_coor(coordinates)
    except:
        return {
                   "message": "Couldn't contact google API"
               }, 401

    group_options = []
    for loc in locs:
        try:
            group = Groups.objects.get(group_id=loc["place_id"])
        except DoesNotExist:
            group = None
            group_user_names = []
        else:
            group_user_names = group.user_names
        user_name = sessions_ids[session_id]
        if user_name not in group_user_names:
            if group:
                group_options.append(group.json())
            else:
                group_options.append({
                    "group_id": loc["place_id"],
                    "group_name": loc["formatted_address"],
                    "group_type": loc["types"][0]
                })
    return group_options, 200
