class UnSupportedCountry(Exception):
    def __init__(self, lat: str, lon: str, country: str):
        super().__init__(f"Country {country} at location {lat}, {lon} not supported.")


class UnknownPlaceType(Exception):
    def __init__(self, type: str):
        super().__init__(f"Unknown place type {type}.")
