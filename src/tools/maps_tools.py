from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from enum import Enum
from langchain_core.tools import tool
from ..config.clients import GMAPS
from ..models.travel_models import Route, Direction
from ..config.settings import PLACES_VISITED, UNITS
import json
from ..config.clients import LLM  # Make sure this path matches where your LLM instance is defined
from langchain.prompts import PromptTemplate


def get_gmaps_client():
    if GMAPS is None:
        raise ValueError("GMAPS client is not initialized. Please check your configuration.")
    return GMAPS

@tool
### Get place details using Google Places API using place_id
def get_place_details(place_id: str) -> Dict[str, Any]:
    """
    Fetches detailed information about a place using its place_id.
    Args:
        place_id (str): The unique identifier for the place.
    Returns:
        Dict[str, Any]: A dictionary containing detailed information about the place.
    """
    place_details = get_gmaps_client().place(place_id=place_id)
    
    if 'result' in place_details:
        result = place_details['result']
        return {
            'name': result.get('name'),
            'address': result.get('formatted_address'),
            'website': result.get('website'),
            'phone_number': result.get('formatted_phone_number')
        }
    
    return {}

### Get nearby places using Google Places API
@tool
def get_nearby_places(lat: float, long: float, radius: int = 5000, place_type: str ='other') -> List[Dict[str, Any]]:
    """
    Fetches nearby places of a specific type using Google Places API.
    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
        radius (int): Search radius in meters.
        place_type (str): The category of places to search for.
    Returns:
        List[Dict[str, Any]]: A list of places with details like place_id, name, latitude, longitude, rating, place_details and price level.
    """
    places_result = get_gmaps_client().places_nearby(
        location=(lat, long),
        radius=radius,
        type=place_type
    )
    
    places_list = []
    for place in places_result.get('results', []):
        if 'geometry' in place and 'location' in place['geometry']:
            location = place['geometry']['location']
            if( place.get('place_id') not in PLACES_VISITED):
                PLACES_VISITED.append(place.get('place_id'))
                places_list.append({
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'latitude': location.get('lat'),
                    'longitude': location.get('lng'),
                    'rating': place.get('rating', 0.0),
                    'place_details' : get_place_details(place.get('place_id')),
                    'price_level': place.get('price_level', 0)
                })
    
    # Sort by rating and then by price level
    places_list.sort(key=lambda x: (-x['rating'], x['price_level']))
    
    return places_list

## Get directions using Google Directions API
@tool
def get_directions(origin: str, destination: str, mode: str = 'driving') -> Route:
    """
    Fetches directions from origin to destination using Google Directions API.
    Args:
        origin (str): The starting address or place.
        destination (str): The ending address or place.
        mode (str): The mode of travel (e.g., 'driving', 'walking', 'bicycling', 'transit').
    Returns:
        Route: A Route object containing the directions, total duration, and distance.
    """
    directions_result = get_gmaps_client().directions(
        origin=origin,
        destination=destination,
        mode=mode,
        units=UNITS,
    )

    if not directions_result:
        print("No directions found.")
        return Route(origin, destination, [], "0 hours", "0 meters")

    route = directions_result[0]
    total_duration = route['legs'][0]['duration']['text']
    total_distance = route['legs'][0]['distance']['text']
    origin_address = route['legs'][0]['start_address']
    destination_address = route['legs'][0]['end_address']
    if route['fare']:
        fare = route['fare']

    directions = []
    for step in route['legs'][0]['steps']:
        direction = Direction(
            distance=step['distance']['text'],
            duration=step['duration']['text'],
            instruction=step['html_instructions'],
            travel_mode=step['travel_mode']
        )
        directions.append(direction)

    return Route(origin_address, destination_address, directions, total_duration, total_duration, fare)



@tool
def calculate_estimated_route_price(origin: str, destination: str, directions: list[Direction], total_duration: str, total_distance: str) -> str:
    """
    Estimates a fair price for transportation based on route details.
    Args:
        origin (str): The starting address or place.
        destination (str): The ending address or place.
        directions (list[Direction]): A list of Direction objects representing each step in the route.
        total_duration (str): The total estimated time to complete the route.
        total_distance (str): The total distance of the route.
        
    Returns:
        str: A JSON string containing the estimated price and currency, or "N/A" if estimation is not possible.
    """
    prompt = (
        """
            You are a professional price estimator for travel routes.
            Based on the following route details, estimate a fair price for transportation.
            Consider factors like distance, duration, and general complexity implied by directions.
            Assume standard vehicle costs (e.g., typical car ride, not luxury or public transit unless specified).
            Provide the estimated price as a numerical value and the currency (e.g., "USD").
            If you cannot estimate, state "N/A".

            Route Details:
            Origin: {origin_address}
            Destination: {destination_address}
            Total Distance: {total_distance}
            Total Duration: {total_duration}
            Directions Summary: {directions}

            Please provide the estimate in the following JSON format:
            {{
                "estimated_price": "numerical_value_or_N/A",
                "currency": "currency_code_or_N/A"
            }}
            """
    )
    template = PromptTemplate(
        input_variables=["origin_address","destination_address","total_distance","total_duration","directions"],
        template=prompt
    )
    response = LLM.invoke(template.format(
        origin_address=origin,
        destination_address=destination,
        total_distance=total_distance,
        total_duration=total_duration,
        directions=directions
    ))
    if response and isinstance(response, str):
        try:
            return json.dumps(response.coptent)
        except ValueError:
            print(f"Could not convert response to float: {response}")
    else:
        print("Invalid response from LLM.")
    return json.dumps({"estimated_price": "N/A","currency": "N/A"})


### Geo Coding Tool 
@tool
def get_geocode_tool(address: str) -> Dict[str, Any]:
    """
    Fetches geographical coordinates (latitude, longitude) for a given address.
    """
    try:
        geocode_result = get_gmaps_client().geocode(address)
        
        if geocode_result:
            print("Geocoding successful!")

            location = geocode_result[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            formatted_address = geocode_result[0]['formatted_address']

            print(f"\nFormatted Address: {formatted_address}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            return {"address": formatted_address, "lat": latitude, "lng": longitude}
        else:
            print("No results found for the given address.")
    except Exception as e:
        print(f"An API error occurred: {e}")
    return {"address": address, "lat": 0.0, "lng": 0.0}

### Reverse Geo Coding Tool 
@tool
def reverse_geocode_tool(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetches a human-readable address for a given latitude and longitude.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        Dict[str, Any]: A dictionary containing the formatted address,
                        latitude, and longitude, or default values if
                        the geocoding fails.
    """
    try:
        gmaps = get_gmaps_client()
        # Perform reverse geocoding
        reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

        if reverse_geocode_result:
            print("Reverse geocoding successful!")
            # The first result is usually the most accurate/relevant one
            formatted_address = reverse_geocode_result[0]['formatted_address']
            # The lat/lng are the input, but we return them for consistency with get_geocoding_tool
            lat = latitude
            lng = longitude

            print(f"\nFormatted Address: {formatted_address}")
            print(f"Latitude: {lat}")
            print(f"Longitude: {lng}")
            return {"address": formatted_address, "lat": lat, "lng": lng}
        else:
            print(f"No address found for coordinates: ({latitude}, {longitude}).")
            return {"address": None, "lat": latitude, "lng": longitude}
    except Exception as e:
        print(f"An API error occurred during reverse geocoding: {e}")
        return {"address": None, "lat": latitude, "lng": longitude}