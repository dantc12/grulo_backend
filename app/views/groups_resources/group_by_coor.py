import json

import requests
from flask_restful import Resource, reqparse

from app.models.groups_model import Groups
from app.sessions_ids import sessions_ids


class GetGroupByCoor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        loc_response = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+args.get('coordinates')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        locations_json = json.loads(response.text)
        for loc in locations_json["results"]:
            try:
                group = Groups.objects.get(groupid=loc["place_id"])
                users = group.users

            except:
                users = []

            if sessions_ids[args.get('session_id')] in users:
                continue
            loc_response.append({"groupid": loc["place_id"], "groupname": loc["formatted_address"], "grouptype": loc["types"][0], "users": users})

        return loc_response, 200