from enum import Enum

class BudgetLevel(Enum):
    """
    Categorizes budget levels into qualitative levels (Low, Medium, High).
    Each level is associated with a typical price level.
    (It is based on the Places API price level).
    """
    LOW = ("Low", 0)       # Price levels 0 to 1
    MEDIUM = ("Medium", 2) # Price levels 2 to 3
    HIGH = ("High", 4)     # Price level 4

    def __init__(self, description: str, min_price_level: int):
        self.description = description
        self.min_price_level = min_price_level

    def __str__(self):
        """Returns the human-readable description of the budget level."""
        return self.description

    @staticmethod
    def from_price_level(price_level: int) -> 'BudgetLevel':
        """
        Determines the BudgetLevel based on a numerical price level.

        Args:
            price_level: An integer representing the price level (e.g., 0 to 4).
                         0 = free, 1 = inexpensive, 2 = moderate, 3 = expensive, 4 = very expensive.

        Returns:
            A BudgetLevel Enum member (LOW, MEDIUM, or HIGH).
            Defaults to LOW for price levels below 0 or unexpected values.
        """
        if price_level >= BudgetLevel.HIGH.min_price_level:
            return BudgetLevel.HIGH
        elif price_level >= BudgetLevel.MEDIUM.min_price_level:
            return BudgetLevel.MEDIUM
        else:
            return BudgetLevel.LOW


class RatingLevel(Enum):
    """
    Categorizes numerical ratings into qualitative levels (Low, Medium, High).
    Each level includes a minimum numerical rating it represents.
    (Assuming a scale typically from 1 to 5, like Google reviews).
    """
    LOW = ("Low", 1.0)        # Ratings from 1.0 up to (but not including) 3.0
    MEDIUM = ("Medium", 3.0)  # Ratings from 3.0 up to (but not including) 4.0
    HIGH = ("High", 4.0)      # Ratings from 4.0 up to 5.0

    def __init__(self, description: str, min_rating_value: float):
        self.description = description
        self.min_rating_value = min_rating_value

    def __str__(self):
        """Returns the human-readable description of the rating level."""
        return self.description
    
    @staticmethod
    def from_numerical_rating(rating: float) -> 'RatingLevel':
        """
        Determines the RatingLevel based on a given numerical rating.

        Args:
            rating: A float representing the numerical rating (e.g., from 1.0 to 5.0).

        Returns:
            A RatingLevel Enum member (LOW, MEDIUM, or HIGH).
            Defaults to LOW for ratings below 1.0 or non-positive.
        """
        if rating >= RatingLevel.HIGH.min_rating_value:
            return RatingLevel.HIGH
        elif rating >= RatingLevel.MEDIUM.min_rating_value:
            return RatingLevel.MEDIUM
        else:
            return RatingLevel.LOW


class AccommodationType(Enum):
    """
    A simple Enum to categorize types of accommodation.
    """
    HOTEL = "Hotel"
    AIRBNB = "Airbnb / Vacation Rental"

    def __str__(self):
        return self.value

class PlaceType(Enum):
    """
    Defines the broad type of a place: either an Attraction or an Activity.
    """
    ATTRACTION = "Attraction"
    ACTIVITY = "Activity"
    ESSENTIAL = "Essential Service"

    def __str__(self):
        return self.value


class PlaceCategory(Enum):
    """
    Defines categories for different types of places
    and a broad PlaceType (Attraction, Activity, or Essential).
    These ENUM's are taken from Google Places API
    https://developers.google.com/maps/documentation/places/web-service/legacy/supported_types\n
    """
    # Enum members now store a tuple (description, place_type)
    CAFE = ("cafe", PlaceType.ACTIVITY)
    RESTAURANT = ("restaurant", PlaceType.ACTIVITY)
    MUSEUM = ("museum", PlaceType.ATTRACTION)
    SUPERMARKET = ("supermarket", PlaceType.ESSENTIAL)
    PARK = ("park", PlaceType.ATTRACTION)
    AQUARIUM = ("aquarium", PlaceType.ACTIVITY)
    BAKERY = ('bakery', PlaceType.ACTIVITY)
    TOURIST_ATTRACTION = ('tourist_attraction', PlaceType.ATTRACTION)
    ZOO = ('zoo', PlaceType.ACTIVITY)
    ART_GALLERY = ('art_gallery', PlaceType.ATTRACTION)
    OTHER = ("other", PlaceType.ACTIVITY)

    def __init__(self, description: str, place_type: PlaceType):
        self.description = description
        self.place_type = place_type

    def get_place_type(self) -> PlaceType:
        return self.place_type

    def __str__(self):
        return self.description