import pytest
from src.tools import util_tools, maps_tools
from src.models.travel_models import Route, Direction

# Mocking external dependencies for isolated unit tests

def test_calculate_average_time_spent_at_an_address(monkeypatch):
    monkeypatch.setattr(util_tools.LLM, "invoke", staticmethod(lambda x: "2.5"))
    result = util_tools.calculate_average_time_spent_at_an_address("museum")
    assert isinstance(result, float)
    assert result == 2.5

def test_convert_unix_to_mmddyyyy():
    unix_timestamp = 1752604800  # 07/15/2025
    result = util_tools.convert_unix_to_mmddyyyy(unix_timestamp)
    assert result == "07/15/2025"

def test_convert_unix_to_yyyymmdd():
    unix_timestamp = 1752604800  # 07/15/2025
    result = util_tools.convert_unix_to_yyyymmdd(unix_timestamp)
    assert result == "2025-07-15"

def test_travel_budget_allocator():
    result = util_tools.travel_budget_allocator(1000, 5, 2, "luxury")
    assert isinstance(result, dict)
    assert "accommodation" in result

def test_add():
    assert util_tools.add(2, 3) == 5

def test_multiply():
    assert util_tools.multiply(2, 3) == 6

def test_get_geocode_tool(monkeypatch):
    class MockGeoCode:
        lat = "40.7128"
        long = "-74.0060"
    monkeypatch.setattr(util_tools, "GeoCode", MockGeoCode)
    result = util_tools.get_geocode_tool("New York")
    assert hasattr(result, "lat")
    assert hasattr(result, "long")

def test_reverse_geocode_tool(monkeypatch):
    monkeypatch.setattr(util_tools.LLM, "invoke", staticmethod(lambda x: "New York, NY"))
    result = util_tools.reverse_geocode_tool(40.7128, -74.0060)
    assert isinstance(result, str)
    assert "New York" in result

def test_get_place_details(monkeypatch):
    monkeypatch.setattr(maps_tools, "get_gmaps_client", lambda: type("GMAPS", (), {"place": staticmethod(lambda place_id: {"result": {"name": "Test Place"}})})())
    result = maps_tools.get_place_details("test_place_id")
    assert isinstance(result, dict)
    assert "name" in result["result"]

def test_get_nearby_places(monkeypatch):
    mock_places = {
        "results": [
            {"place_id": "1", "name": "Place 1", "geometry": {"location": {"lat": 1, "lng": 2}}, "rating": 4.5, "price_level": 2}
        ]
    }
    monkeypatch.setattr(maps_tools, "get_gmaps_client", lambda: type("GMAPS", (), {"places_nearby": staticmethod(lambda **kwargs: mock_places)})())
    result = maps_tools.get_nearby_places(1.0, 2.0, 5000, "restaurant")
    assert isinstance(result, list)
    assert result[0]["name"] == "Place 1"

def test_get_directions(monkeypatch):
    mock_result = {
        "routes": [{
            "legs": [{
                "distance": {"text": "5 mi"},
                "duration": {"text": "20 mins"},
                "steps": [
                    {"html_instructions": "Head north", "distance": {"text": "1 mi"}, "duration": {"text": "5 mins"}, "travel_mode": "DRIVING"}
                ]
            }]
        }]
    }
    monkeypatch.setattr(maps_tools, "get_gmaps_client", lambda: type("GMAPS", (), {"directions": staticmethod(lambda **kwargs: mock_result)})())
    result = maps_tools.get_directions("A", "B", "driving")
    assert isinstance(result, dict)
    assert "directions" in result

def test_calculate_estimated_route_price():
    # Minimal mock Route object
    route = Route(
        origin_add="A",
        destination_add="B",
        directions=[Direction(distance="5 mi", duration="20 mins", instruction="Head north", travel_mode="DRIVING")],
        total_duration="20 mins",
        total_distance="5 mi",
        fare={"amount": 0}
    )
    result = maps_tools.calculate_estimated_route_price(route)
    assert isinstance(result, float)

def test_hotel_search_tool(monkeypatch):
    mock_hotels = [
        {"name": "Hotel Luxury", "address": "123 Main St", "rating": 4.8, "price": 500}
    ]
    monkeypatch.setattr(maps_tools, "hotel_search_tool", staticmethod(lambda location, adults, checkin, checkout: mock_hotels))
    result = maps_tools.hotel_search_tool("NYC", 2, "2025-07-15", "2025-07-19")
    assert isinstance(result, list)
    assert result[0]["name"] == "Hotel Luxury"

def test_get_weather_and_forecast(monkeypatch):
    mock_weather = {
        "date": "2025-07-15",
        "condition": "Sunny",
        "high": 95,
        "low": 78
    }
    monkeypatch.setattr(maps_tools, "get_weather_and_forecast", staticmethod(lambda location, date: mock_weather))
    result = maps_tools.get_weather_and_forecast("NYC", "2025-07-15")
    assert isinstance(result, dict)
    assert result["condition"] == "Sunny"

def test_estimate_hotel_cost(monkeypatch):
    monkeypatch.setattr(maps_tools, "estimate_hotel_cost", staticmethod(lambda hotel_name, checkin, checkout, num_adults: 2000))
    result = maps_tools.estimate_hotel_cost("Hotel Luxury", "2025-07-15", "2025-07-19", 2)
    assert isinstance(result, int) or isinstance(result, float)
    assert result