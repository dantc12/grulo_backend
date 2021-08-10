from typing import List, Optional

from pydantic import BaseModel


class GoogleAddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: List[str]


class GoogleGeocodeResult(BaseModel):
    address_components: List[GoogleAddressComponent]
    formatted_address: str
    place_id: str
    types: List[str]
    plus_code: Optional[dict] = None
