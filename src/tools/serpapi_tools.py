from langchain_core.tools import tool
from ..config.settings import SERP_API_KEY
from .maps_tools import reverse_geocode_tool
from datetime import datetime
from serpapi import GoogleSearch

@tool
def hotel_search_tool(location: str, adults: int = 1, checkin: str = None, checkout: str = None) -> list:
    """
    Searches for hotels using the SerpAPI Google Hotels API.

    Args:
        location (str): The destination city name or IATA code (e.g., "Paris", "NYC").
                        SerpAPI is more flexible with location names.
        adults (int): Number of adults (default: 1).
        checkin (str): Check-in date in 'YYYY-MM-DD' format. If None, defaults to tomorrow.
        checkout (str): Check-out date in 'YYYY-MM-DD' format. If None, defaults to day after tomorrow.

    Returns:
        list: A list of dictionaries, each representing a hotel with its name, address,
              rating, total price, average daily price, and a summary of amenities.
              Returns an empty list if no hotels are found or an error occurs.
    """

    if not SERP_API_KEY:
        return [{"error": "SerpAPI client not initialized. Check API key."}]

    # Validate and set default dates if not provided
    if checkin is None:
        checkin_date_obj = datetime.now() + timedelta(days=1)
        checkin_date = checkin_date_obj.strftime('%Y-%m-%d')
    else:
        try:
            checkin_date_obj = datetime.strptime(checkin, '%Y-%m-%d')
            checkin_date = checkin_date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return [{"error": "Invalid check-in date format. Use YYYY-MM-DD."}]

    if checkout is None:
        checkout_date_obj = checkin_date_obj + timedelta(days=1) # Default to 1 night stay
        checkout_date = checkout_date_obj.strftime('%Y-%m-%d')
    else:
        try:
            checkout_date_obj = datetime.strptime(checkout, '%Y-%m-%d')
            checkout_date = checkout_date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return [{"error": "Invalid check-out date format. Use YYYY-MM-DD."}]


    try:

        # Construct SerpAPI parameters for Google Hotels
        params = {
            "engine": "google_hotels",
            "q": f"hotels in {location}",
            "check_in_date": checkin_date,
            "check_out_date": checkout_date,
            "adults": adults,
            "api_key": SERP_API_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        hotels = []
        if "properties" in results:
            # Sort properties by rating if available, otherwise by overall score
            # Google Hotels from SerpAPI usually provides 'overall_rating' or 'star_rating'
            sorted_properties = sorted(
                results["properties"],
                key=lambda x: x.get('overall_rating', 0) or x.get('star_rating', 0),
                reverse=True
            )

            for hotel_data in sorted_properties:
                hotel_info = {
                    "hotel_name": hotel_data.get("name"),
                    "address": reverse_geocode_tool.invoke({'latitude':hotel_data.get("gps_coordinates", {}).get("latitude"), 'longitude':hotel_data.get("gps_coordinates", {}).get("longitude")}),
                    "latitude": hotel_data.get("gps_coordinates", {}).get("latitude"),
                    "longitude": hotel_data.get("gps_coordinates", {}).get("longitude"),
                    "rating": hotel_data.get("overall_rating"),
                    "total_rate": hotel_data.get("total_rate", {}).get("lowest"),
                    "extracted_hotel_class": hotel_data.get("extracted_hotel_class"),
                    "amenities": hotel_data.get("amenities", [])
                }
                hotels.append(hotel_info)

            return hotels
        else:
            return [{"message": "No hotel offers found for the specified criteria."}]

    except Exception as e:
        print(f"An unexpected error occurred with SerpAPI: {e}")
        return [{"error": f"An unexpected error occurred with SerpAPI: {e}"}]