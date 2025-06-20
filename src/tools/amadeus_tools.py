from typing import List, Optional
from langchain_core.tools import tool
from amadeus import ResponseError, Location
from ..models.amadeus_models import FlightOffer
from ..config.clients import AMADEUS_CLIENT
from ..config.settings import BASE_CURRENCY

@tool
def get_airport_name(iata_code: str) -> str:
    """
    Fetches the name of an airport using its IATA code.
    Args:
        iata_code (str): The IATA code of the Airport.
    Returns:
        str: The name of the airport location, or the IATA code if not found or an error occurs.
    """
    if AMADEUS_CLIENT is None:
        return iata_code # Cannot fetch without client

    try:
        response = AMADEUS_CLIENT.reference_data.locations.get(keyword=iata_code, subType=Location.AIRPORT)
        if response.data:
            return response.data[0].get('name', iata_code)
        else:
            return iata_code
    except ResponseError as e:
        print(f"Error fetching airport name for {iata_code}: {e}")
        return iata_code

@tool
def get_airline_name(iata_code: str) -> str:
    """
    Fetches the name of an airline using its IATA code.
    Args:
        iata_code (str): The IATA code of the Airline.
    Returns:
        str: The name of the airline, or the IATA code if not found or an error occurs.
    """
    if AMADEUS_CLIENT is None:
        return iata_code # Cannot fetch without client

    try:
        response = AMADEUS_CLIENT.reference_data.airlines.get(airlineCodes=iata_code)
        if response.data:
            return response.data[0].get('businessName', iata_code)
        else:
            return iata_code
    except ResponseError as e:
        print(f"Error fetching airline name for {iata_code}: {e}")
        return iata_code

@tool
def get_flight_details(origin: str, destination: str, departure_date: str, return_date: Optional[str] = None, num_guests: int = 1) -> List[FlightOffer]:
    """
    Fetches flight details using Amadeus API.
    Args:
        origin (str): The IATA code of the origin airport.
        destination (str): The IATA code of the destination airport.
        departure_date (str): The departure date in YYYY-MM-DD format.
        return_date (Optional[str]): The return date in YYYY-MM-DD format. If None, one-way flight is assumed.
        num_guests (int): Number of guests traveling.
    Returns:
        List[FlightOffer]: A list of FlightOffer objects containing flight details.
    """
    if AMADEUS_CLIENT is None:
        print("Amadeus client not initialized. Cannot fetch flight details.")
        return []

    try:
        response = AMADEUS_CLIENT.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            returnDate=return_date,
            adults=num_guests,
            travelClass='ECONOMY',
            max=5,
            currencyCode=BASE_CURRENCY,
        )
        if response.data:
            return [FlightOffer.model_validate(offer) for offer in response.data]
        else:
            print("No flight offers found.")
            return []
    except ResponseError as e:
        print(f"Error fetching flight details: {e}")
        return []