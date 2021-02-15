import json
from typing import Dict, List

import requests


def get_google_maps_coors(coor_str: str) -> List[Dict]:
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
          "{}&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(coor_str)
    response = requests.request("GET", url, headers={}, data={})
    locations_json = json.loads(response.text)
    return locations_json.get("results")


def get_google_maps_group(group_id: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json?place_id={}" \
          "&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(group_id)
    response = requests.request("GET", url, headers={}, data={})
    response_json = json.loads(response.text)
    group_name = response_json["results"][0]["formatted_address"]
    group_type = response_json["results"][0]["types"][0]
    return group_name, group_type
