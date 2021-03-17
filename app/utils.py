import json
from typing import Dict, List

import requests

from app.sessions_ids import sessions_ids


def get_google_groups_by_coor(coor_str: str) -> List[Dict]:
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
          "{}&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(coor_str)
    response = requests.request("GET", url, headers={}, data={})
    locations_json = json.loads(response.text)
    return locations_json.get("results")


def get_google_group_by_id(group_id: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json?place_id={}" \
          "&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(group_id)
    response = requests.request("GET", url, headers={}, data={})
    response_json = json.loads(response.text)
    group_name = response_json["results"][0]["formatted_address"]
    group_type = response_json["results"][0]["types"][0]
    return group_name, group_type


def get_google_groups_by_addr(address: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}" \
          "&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(address)
    response = requests.request("GET", url, headers={}, data={})

    search_results = json.loads(response.text)["results"]
    return search_results


def check_if_logged_in(session_id: str):
    if session_id not in sessions_ids.keys():
        return {
                   "message": "Not logged in"
        }, 400
    else:
        return {}, 200
