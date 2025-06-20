from src.models.openweather_models import OpenWeatherResponse
from src.models.amadeus_models import FlightOffer
from typing import List, Optional, Dict, Any, TypedDict
from langchain_core.messages import BaseMessage

class TravelAgentState(TypedDict):
    """
    Represents the state of the travel planning process.
    This object will be passed between nodes and updated.
    """
    user_query: str # The initial query from the user
    origin: Optional[str]
    destination: Optional[str]
    start_date: Optional[str] # Changed to str for simplicity with date parsing from user input
    end_date: Optional[str] # Changed to str for simplicity with date parsing from user input
    num_guests: Optional[int]
    preferences: List[str] # e.g., ["culture", "foodie", "adventure"]
    native_currency: str # The user's preferred currency for expense calculation

    # Information gathered by agents/tools (will be populated as the graph runs)
    weather_info: Optional[OpenWeatherResponse] # Stores current and forecast weather
    flights_info: Optional[List[FlightOffer]] # Stores flight details (changed to List[Dict] as FlightOffer is a Pydantic model)
    attractions: List[Dict[str, Any]] # List of discovered attractions
    restaurants: List[Dict[str, Any]] # List of discovered restaurants
    activities: List[Dict[str, Any]] # List of discovered activities
    hotels: List[Dict[str, Any]] # Raw search results for hotels
    selected_hotel: Optional[Dict[str, Any]] # The chosen hotel details
    estimated_costs: List[Dict[str, Any]] # List of individual expenses (e.g., hotel, food, activities)
    total_estimated_cost: Optional[float] # Sum of all estimated expenses in native currency
    itinerary_draft: List[Dict[str, Any]] # The day-by-day itinerary
    final_summary: Optional[str] # The comprehensive summary of the trip

    # For conversational flow and debugging
    messages: List[BaseMessage] # A history of messages, including LLM responses and tool calls/outputs
