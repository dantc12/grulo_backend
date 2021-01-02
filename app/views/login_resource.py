from flask_restful import Resource, reqparse
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

        print(Users.objects.get(username=args.get('username'))["password"])

        if Users.objects.get(username=args.get('username'))["password"] == args.get('password'):
            session_id = str(binascii.hexlify(os.urandom(24)).decode('ascii'))

            sessions_ids[session_id] = args.get('username')

            # with open('sessions_ids.py') as json_file:
            #     sessions_data = json.load(json_file)
            #
            # with open('sessions_ids.py', 'w') as outfile:
            #     sessions_data[args.get('username')] = session_id
            #     json.dump(sessions_data, outfile)

            return {"session_id": session_id}, 200

        else:
            return "Password is incorrect", 403
