from app.models.groups_model import Groups
import json
from app.sessions_ids import sessions_ids


def get_all_groups(session_id: str):
    if session_id not in sessions_ids.keys():
        return {
            "message": "Not logged in"
        }, 400
    groups = Groups.objects()
    return json.loads(groups.to_json()), 200
