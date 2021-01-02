import json

import requests
from flask_restful import Resource, reqparse

from app.models.groups_model import Groups


class SearchGroup(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        results_json = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+args.get('address')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        search_results = json.loads(response.text)
        for result in search_results["results"]:
            try:
                group = Groups.objects.get(groupid=result["place_id"])
                users = group.users

            except:
                users = []
            results_json.append({"groupname": result["formatted_address"], "groupid": result["place_id"], "grouptype": result["types"][0], "user": users})

            address_componets = {}
            sub_address = []

            for components in result["address_components"]:
                address_componets[components["types"][0]] = components["long_name"]

            if "street_number" in address_componets.keys():
                sub_address.append("{0}, {1}, {2}".format(address_componets["route"], address_componets["locality"], address_componets["country"]))
            if "route" in address_componets.keys():
                sub_address.append("{0}, {1}".format(address_componets["locality"], address_componets["country"]))
            if "locality" in address_componets.keys():
                print("found country")
                sub_address.append("{0}".format(address_componets["country"]))

            [sub_address.append(val) for key, val in address_componets.items() if "administrative_area" in key]

            for sub_addr in sub_address:
                print(sub_address)
                url = "https://maps.googleapis.com/maps/api/geocode/json?address="+sub_addr+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"

                response_sub = requests.request("GET", url, headers=headers, data=payload)

                search_results_sub = json.loads(response_sub.text)
                for result_sub in search_results_sub["results"]:
                    try:
                        group = Groups.objects.get(groupid=result_sub["place_id"])
                        users = group.users

                    except:
                        users = []
                    results_json.append({"groupname": result_sub["formatted_address"], "groupid": result_sub["place_id"], "grouptype": result_sub["types"][0], "user": users})

        return {"message": "Found {0} Groups.".format(len(results_json)),"results":results_json}, 200