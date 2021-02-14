import json
from typing import Dict, List

import requests


def get_google_maps_coors(coor_str: str) -> List[Dict]:
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
          "{}&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw".format(coor_str)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    locations_json = json.loads(response.text)

    return locations_json.get("results")
