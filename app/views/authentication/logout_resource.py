from typing import Dict

from app.sessions_ids import sessions_ids


def logout(logout_info: Dict):
    session_id = logout_info.get("session_id")
    _ = sessions_ids[session_id]
    del sessions_ids[session_id]

    return {}, 200
