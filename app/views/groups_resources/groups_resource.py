from app.models.groups_model import Groups
import json
from app.utils import check_if_logged_in


def get_all_groups(session_id: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    groups = Groups.objects()
    return json.loads(groups.to_json()), 200
