from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist

from app.models.groups_model import Groups
from app.sessions_ids import sessions_ids
from app.utils import get_google_maps_coors


class GetGroupsByCoor(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        loc_response = []

        locs = get_google_maps_coors(args.get('coordinates'))

        for loc in locs:
            try:
                group = Groups.objects.get(groupid=loc["place_id"])
            except DoesNotExist:
                raise Exception("Issue with getting google group from grulo groups db.")

            users = group.users
            username = sessions_ids[args.get('session_id')]

            if username not in users:
                loc_response.append({
                    "groupid": loc["place_id"],
                    "groupname": loc["formatted_address"],
                    "grouptype": loc["types"][0],
                    "users": users})

        return {"data": loc_response}, 200
