
from .enums import BudgetLevel
from pydantic import BaseModel
from typing import Dict, Optional

class TravelBudgetAllocator(BaseModel):
    total_budget: float
    trip_type: str
    duration_days: int
    category_weights: Optional[Dict[str, float]] = None

    def __init__(self, total_budget: float, trip_type: str, duration_days: int, category_weights: Optional[Dict[str, float]] = None):
        # Convert trip_type to Enum if needed
        if isinstance(trip_type, str):
            try:
                trip_type_enum = BudgetLevel(trip_type)
            except ValueError:
                trip_type_enum = BudgetLevel.MEDIUM  # or some default
        else:
            trip_type_enum = trip_type
        super().__init__(
            total_budget=total_budget,
            trip_type=trip_type_enum,
            duration_days=duration_days,
            category_weights=category_weights
        )
        object.__setattr__(self, 'category_weights', self._set_base_weights())

    def _set_base_weights(self) -> dict:
        base = {
            "accommodation": 0.35,
            "transportation": 0.25,
            "food": 0.15,
            "activities": 0.15,
            "miscellaneous": 0.10
        }
        return self._adjust_weights(base)

    def _adjust_weights(self, weights: dict) -> dict:
        if self.trip_type == BudgetLevel.HIGH:
            weights["accommodation"] += 0.1
            weights["food"] += 0.05
            weights["miscellaneous"] -= 0.05
        elif self.trip_type == BudgetLevel.MEDIUM:
            weights["transportation"] += 0.1
            weights["accommodation"] -= 0.05
        elif self.trip_type == BudgetLevel.LOW:
            weights["miscellaneous"] += 0.05
            weights["food"] -= 0.05
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def allocate(self) -> dict:
        return {
            category: round(weight * self.total_budget, 2)
            for category, weight in self.category_weights.items()
        }

class GeoCode(BaseModel):
    lat: str
    long: str

    def __str__(self):
        if not self.lat or not self.long:
            return "GeoCode not set"
        return f"Latitude: {self.lat}, Longitude: {self.long}"

class Direction(BaseModel):
    distance: str
    duration: str
    instruction: str
    travel_mode: str

    def __str__(self):
        return (f"  - {self.instruction} ({self.travel_mode}): "
                f"Distance: {self.distance}, Duration: {self.duration}")

class Route(BaseModel):
    origin_add: str
    destination_add: str
    directions: list[Direction]
    total_duration: str
    total_distance: str
    fare: dict

    def __str__(self):
        if not self.origin_add or not self.destination_add or not self.directions:
            return "Route not set"
        directions_str = "\n".join(str(d) for d in self.directions)
        return (f"Route from: {self.origin_add}\n"
                f"To: {self.destination_add}\n"
                f"Total Distance: {self.total_distance}\n"
                f"Total Duration: {self.total_duration}\n"
                f"Directions:\n{directions_str}")