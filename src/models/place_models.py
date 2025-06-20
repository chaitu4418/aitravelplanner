from pydantic import BaseModel
from typing import Optional

class LatLng(BaseModel):
    lat: float
    lng: float

class Geometry(BaseModel):
    location: LatLng

class PlaceDetails(BaseModel):
    # Direct fields from the 'result' object
    formatted_address: str
    formatted_phone_number: Optional[str] = None
    name: str
    place_id: str
    website: Optional[str] = None
    
class Place(BaseModel):
    business_status: str
    geometry: Geometry
    name: str
    place_id: str
    rating: float
    user_ratings_total: int
    place_details: PlaceDetails