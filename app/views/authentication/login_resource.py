from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.users_model import Users
import os
import binascii

from app.sessions_ids import sessions_ids


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        try:
            u = Users.objects.get(username=args.get('username'))
        except DoesNotExist:
            return {"message": "User or password are incorrect."}, 500
        else:
            if u["password"] == args.get('password'):
                for session_id, username in sessions_ids.items():
                    if u.username == username:
                        return {"message": "Login successful.",
                                "session_id": session_id}, 200
                session_id = str(binascii.hexlify(os.urandom(24)).decode('ascii'))
                sessions_ids[session_id] = args.get('username')
                return {"message": "Login successful.",
                        "session_id": session_id}, 200
            else:
                return {"message": "User or password are incorrect."}, 500
