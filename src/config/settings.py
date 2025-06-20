import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and Client IDs
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
GOOGLECLOUD_API_KEY = os.getenv('GOOGLECLOUD_API_KEY')
AMADEUS_CLIENT_ID = os.getenv('AMADEUS_CLIENT_ID')
AMADEUS_CLIENT_SECRET = os.getenv('AMADEUS_CLIENT_SECRET')
SERP_API_KEY = os.getenv('SERP_API_KEY')

# Default Configuration Settings
BASE_CURRENCY = os.getenv('BASE_CURRENCY', 'USD')  # Default currency for expenses and flights
UNITS = os.getenv('UNITS', 'IMPERIAL')             # Units system for weather and distances ('METRIC' or 'IMPERIAL')

# Default Geographical Coordinates (e.g., for initial weather/places lookup if not specified)
# Default Plano, TX
LAT = float(os.getenv('DEFAULT_LAT', 33.0217))
LONG = float(os.getenv('DEFAULT_LONG', -96.6980))

# Global lists/variables that might need to persist state or track data
PLACES_VISITED = [] # To keep track of places already suggested/visited to avoid repetition