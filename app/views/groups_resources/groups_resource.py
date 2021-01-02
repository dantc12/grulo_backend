from flask_restful import Resource, reqparse
from app.models.groups_model import Groups
import json
from app.sessions_ids import sessions_ids

class GetAllGroups(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()  # parse arguments to dictionary
        groups = Groups.objects()
        return json.loads(groups.to_json()), 200
