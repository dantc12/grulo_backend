from typing import List, Set

import requests

from .place import Place
from . import exceptions
from .reverse_geocoder import ReverseGeocoder
from .schemas import GoogleGeocodeResult


class GoogleGeocoder(ReverseGeocoder):
    _url: str
    _api_key: str
    _types_map: dict
    _supported_country: str

    def __init__(self, url: str, api_key: str, types_map: dict, supported_country: str):
        self._url = url
        self._api_key = api_key
        self._types_map = types_map
        self._supported_country = supported_country

    def _safe_create_place(self, name: str, type: str) -> Place:
        mapped = self._types_map.get(type)
        if mapped is None:
            raise exceptions.UnknownPlaceType(type)
        return Place(name, mapped)

    def _parse_google_result(self, result: GoogleGeocodeResult) -> Set[Place]:
        places = set()
        if "street_number" not in result.address_components[0].types or "route" in result.types:
            return places
        country = result.address_components[-1]
        places.add(self._safe_create_place(country.long_name, country.types[0]))
        sub_locations = result.address_components[-2:0:-1]
        place_name = country.long_name
        for sub_location in sub_locations:
            place_name = f"{sub_location.long_name}, {place_name}"
            places.add(self._safe_create_place(place_name, sub_location.types[0]))
        places.add(self._safe_create_place(result.formatted_address, "street_address"))
        return places

    def reverse_geocode(self, lat: str, lon: str) -> List[Place]:
        response = requests.get(self._url, params={
            "key": self._api_key,
            "latlng": f"{lat},{lon}",
            "language": "iw"
        })
        response.raise_for_status()
        google_results = response.json().get("results")
        places = set()
        for result in google_results:
            result = GoogleGeocodeResult(**result)
            if result.address_components[-1].long_name != self._supported_country:
                raise exceptions.UnSupportedCountry(lat, lon, result.address_components[-1].long_name)
            places = places.union(self._parse_google_result(result))
        return list(places)
