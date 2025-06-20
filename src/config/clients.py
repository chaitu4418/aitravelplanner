import os
import googlemaps
import amadeus
from langchain_openai import ChatOpenAI

# Import settings to get API keys and default values
from .settings import (
    GOOGLECLOUD_API_KEY,
    OPENWEATHER_API_KEY,
    EXCHANGERATE_API_KEY,
    AMADEUS_CLIENT_ID,
    AMADEUS_CLIENT_SECRET,
    BASE_CURRENCY,
    UNITS,
    LAT,
    LONG,
)

# --- 1. Initialize API Clients and URLs ---

# Initialize the Google Maps client
GMAPS = None
if GOOGLECLOUD_API_KEY is None:
    print("Error: GOOGLECLOUD_API_KEY environment variable not set. Google Maps client will not be initialized.")
else:
    GMAPS = googlemaps.Client(key=GOOGLECLOUD_API_KEY)

# Initialize The OpenWeather API URL
OPENWEATHER_BASEURL = None
if OPENWEATHER_API_KEY is None:
    print("Error: OPENWEATHER_API_KEY environment variable not set. OpenWeather API URL will not be initialized.")
else:
    # Note: The original notebook had a typo 'exchangerate_baseurl' for OpenWeather. Correcting it here.
    OPENWEATHER_BASEURL = f'https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LONG}&appid={OPENWEATHER_API_KEY}&units={UNITS}'

# Initialize the Exchange Rate API URL
EXCHANGERATE_BASERURL = None
if EXCHANGERATE_API_KEY is None:
    print("Error: EXCHANGERATE_API_KEY environment variable not set. ExchangeRate API URL will not be initialized.")
else:
    EXCHANGERATE_BASERURL = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{BASE_CURRENCY}'

# Initialize the Amadeus client
AMADEUS_CLIENT = None
if AMADEUS_CLIENT_ID is None or AMADEUS_CLIENT_SECRET is None:
    print("Error: AMADEUS_CLIENT_ID & AMADEUS_CLIENT_SECRET environment variables not set. Amadeus client will not be initialized.")
else:
    AMADEUS_CLIENT = amadeus.Client(client_id=AMADEUS_CLIENT_ID, client_secret=AMADEUS_CLIENT_SECRET)
    
# Initialize the OpenAI client
if os.getenv('OPENAI_API_KEY') is None:
    print("Error: OPENAI_API_KEY environment variable not set.")
    
LLM = ChatOpenAI(model_name="gpt-4o", temperature=0.2)