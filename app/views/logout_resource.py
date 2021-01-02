from flask_restful import Resource, reqparse
from app.sessions_ids import sessions_ids


class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()

        username = sessions_ids[args['session_id']]
        del sessions_ids[args['session_id']]

        response = {"message": "Logged out {} successfully.".format(username)}
        return response, 200
