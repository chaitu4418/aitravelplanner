import requests
from langchain_core.tools import tool
from ..config.clients import OPENWEATHER_BASEURL
from ..models.openweather_models import OpenWeatherResponse
from ..config.settings import UNITS, OPENWEATHER_API_KEY

### Get current weather and forecast using OpenWeather One Call API
@tool
def get_weather_and_forecast(lat: float,long: float, metric: str = UNITS) -> OpenWeatherResponse:
    '''
    Fetches current weather conditions using the OpenWeather One Call API.
    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
    Returns:
        OpenWeatherOneCallAPIResponse: Parsed response containing current weather data.
    '''
    if not OPENWEATHER_BASEURL:
        raise ValueError("OPENWEATHER_BASEURL is not set or is None.")
    params = {
        "lat": lat,
        "lon": long,
        "appid": OPENWEATHER_API_KEY,
        "units": metric
    }
    response = requests.get(OPENWEATHER_BASEURL, params=params)
    response.raise_for_status()
    return OpenWeatherResponse.model_validate(response.json())