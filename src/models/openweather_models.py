# src/models/openweather_models.py
from pydantic import BaseModel
from typing import List, Optional

class Weather(BaseModel):
    """Represents a single weather condition."""
    main: str
    description: str

class Temperature(BaseModel):
    """Represents temperature values for daily forecast."""
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float

class FeelsLike(BaseModel):
    """Represents 'feels like' temperature values for daily forecast."""
    day: float
    night: float
    eve: float
    morn: float

class CurrentWeather(BaseModel):
    """Model for current weather conditions."""
    dt: int  # Current time, Unix, UTC
    temp: float
    feels_like: float
    clouds: int 
    visibility: int
    wind_speed: float
    weather: List[Weather]

class DailyForecast(BaseModel):
    """Model for daily forecast for 8 days."""
    dt: int  # Time of the forecasted data, Unix, UTC
    summary: Optional[str] = None # Human-readable description (new in OWM 3.0)
    temp: Temperature
    feels_like: FeelsLike
    clouds: int
    weather: List[Weather]

class OpenWeatherResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    current: Optional[CurrentWeather] = None
    daily: Optional[List[DailyForecast]] = None