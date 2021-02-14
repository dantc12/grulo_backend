from typing import Dict

from mongoengine import DoesNotExist

from app.models.users_model import Users
import os
import binascii

from app.sessions_ids import sessions_ids


def login(login_info: Dict):
    try:
        u = Users.objects.get(user_name=login_info.get('user_name'))
    except DoesNotExist:
        return {"message": "User or password are incorrect."}, 500
    else:
        if u["password"] == login_info.get('password'):
            for session_id, user_name in sessions_ids.items():
                if u.user_name == user_name:
                    return {
                        "session_id": session_id
                    }, 200
            session_id = str(binascii.hexlify(os.urandom(24)).decode('ascii'))
            sessions_ids[session_id] = login_info.get('user_name')
            return {
                "session_id": session_id
            }, 200
        else:
            return {"message": "User or password are incorrect."}, 500
