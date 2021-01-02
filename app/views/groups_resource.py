from flask_restful import Resource, reqparse
from app.models.groups_model import Groups
import requests
import json

class GetByCoor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        loc_response = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+args.get('coordinates')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        locations_json = json.loads(response.text)
        for loc in locations_json["results"]:
            loc_response.append({"groupid": loc["place_id"], "groupname": loc["formatted_address"], "grouptype": loc["types"][0]})

        return loc_response, 200

        