from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.groups_model import Groups


class GroupById(Resource):
    def get(self, groupid):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            g = Groups.objects.get(groupid=groupid)
        except DoesNotExist:
            return {"message": "Group doesn't exist."}, 500
        else:
            response = {"message": "Found group successfully."}
            response.update(g.json())
            return response, 200
