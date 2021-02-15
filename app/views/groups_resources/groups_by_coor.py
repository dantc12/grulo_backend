from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.sessions_ids import sessions_ids
from app.utils import get_google_maps_coors


def get_groups_by_coor(session_id: str, coordinates: str):
    try:
        locs = get_google_maps_coors(coordinates)
    except:
        return {
            "message": "Couldn't couldn't contact google API"
        }, 400

    groups_res = []
    for loc in locs:
        try:
            group = Groups.objects.get(group_id=loc["place_id"])
        except DoesNotExist:
            return {
                "message": "Issue with getting google group from grulo groups db."
            }, 400
        users = group.users
        user_name = sessions_ids[session_id]
        if user_name not in [u.user_name for u in users]:
            groups_res.append({
                "group_id": loc["place_id"],
                "group_name": loc["formatted_address"],
                "group_type": loc["types"][0]
            })

    return groups_res, 200
