from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

## Flights Model
# --- Pydantic Models ---

class BaggageAllowance(BaseModel):
    """Represents included baggage quantities."""
    quantity: int

class Amenity(BaseModel):
    """Represents an amenity offered for a segment."""
    description: str
    isChargeable: bool

class SegmentPricingDetails(BaseModel):
    """Details specific to pricing and amenities for a traveler's segment."""
    segmentId: str
    cabin: str
    includedCheckedBags: Optional[BaggageAllowance] = None
    includedCabinBags: Optional[BaggageAllowance] = None
    amenities: List[Amenity] = [] # List of amenities, can be empty

class TravelerPricing(BaseModel):
    """Pricing details for a specific traveler."""
    travelerId: str
    fareDetailsBySegment: List[SegmentPricingDetails]

class DepartureArrivalLocation(BaseModel):
    """Details for departure/arrival airport."""
    iataCode: str
    terminal: Optional[str] = None
    at: str

class Segment(BaseModel):
    """Represents a single flight segment."""
    departure: DepartureArrivalLocation
    arrival: DepartureArrivalLocation
    carrierCode: str # Actual carrier
    number: str # Flight number
    operating: Optional[Dict[str, str]] = None 
    duration: str 
    id: str 
    @property
    def operating_carrier_code(self) -> Optional[str]:
        return self.operating.get('carrierCode') if self.operating else None

class Itinerary(BaseModel):
    """Represents a sequence of segments for a journey."""
    duration: str
    segments: List[Segment]

class Price(BaseModel):
    """Represents pricing information."""
    currency: str
    grandTotal: str

class FlightOffer(BaseModel):
    """
    Main Pydantic model for a simplified Amadeus flight offer,
    capturing the requested fields.
    """
    flight_id: str = Field(..., alias='id')
    itineraries: List[Itinerary]
    price: Price
    travelerPricings: List[TravelerPricing]

    @property
    def origin(self) -> Optional[str]:
        """Returns the Airport Name/IATA code of the first segment's departure airport."""
        if self.itineraries and self.itineraries[0].segments:
            return self.itineraries[0].segments[0].departure.iataCode
        return None

    @property
    def destination(self) -> Optional[str]:
        """Returns the Airport Name/IATA of the last segment's arrival airport."""
        if self.itineraries and self.itineraries[0].segments:
            return self.itineraries[0].segments[-1].arrival.iataCode
        return None

    @property
    def departure_date(self) -> Optional[str]:
        """Returns the departure date of the first segment."""
        if self.itineraries and self.itineraries[0].segments:
            return self.itineraries[0].segments[0].departure.at.split('T')[0]
        return None

    @property
    def arrival_date(self) -> Optional[str]:
        """Returns the arrival date of the last segment."""
        if self.itineraries and self.itineraries[0].segments:
            return self.itineraries[0].segments[-1].arrival.at.split('T')[0]
        return None

    @property
    def currency(self) -> str:
        """Returns the currency of the offer."""
        return self.price.currency

    @property
    def duration(self) -> str:
        """Returns the total duration of the first itinerary."""
        if self.itineraries:
            return self.itineraries[0].duration
        return "N/A"

    @property
    def grandTotal(self) -> str:
        """Returns the grand total price."""
        return self.price.grandTotal

    @property
    def segments_info(self) -> List[Dict[str, Any]]:
        """
        Extracts detailed segment information including cabin, baggage, and amenities
        by mapping traveler pricing details back to segments.
        Assumes pricing details are for the first traveler.
        """
        all_segments_info = []
        if not self.itineraries:
            return []

        # Assuming the first itinerary is the primary one and first traveler's pricing
        main_itinerary = self.itineraries[0]
        first_traveler_pricing = self.travelerPricings[0] if self.travelerPricings else None

        for segment in main_itinerary.segments:
            segment_details: Dict[str, Any] = {
                "departure": segment.departure.iataCode,
                "arrival": segment.arrival.iataCode,
                "carrierCode": segment.carrierCode,
                "number": segment.number,
                "operating_carrier_code": segment.operating_carrier_code,
                "duration_segment": segment.duration, # Duration for this specific segment
            }

            # Find corresponding pricing details for this segment
            if first_traveler_pricing:
                segment_pricing_detail = next(
                    (spd for spd in first_traveler_pricing.fareDetailsBySegment if spd.segmentId == segment.id),
                    None
                )
                if segment_pricing_detail:
                    segment_details["cabin"] = segment_pricing_detail.cabin
                    segment_details["includedCheckedBags"] = segment_pricing_detail.includedCheckedBags.quantity if segment_pricing_detail.includedCheckedBags else 0
                    segment_details["includedCabinBags"] = segment_pricing_detail.includedCabinBags.quantity if segment_pricing_detail.includedCabinBags else 0
                    segment_details["amenities"] = [
                        {"description": a.description, "isChargeable": a.isChargeable}
                        for a in segment_pricing_detail.amenities
                    ]
                else:
                    # Provide defaults if pricing details not found for segment
                    segment_details["cabin"] = "N/A"
                    segment_details["includedCheckedBags"] = 0
                    segment_details["includedCabinBags"] = 0
                    segment_details["amenities"] = []
            else:
                # No traveler pricing available at all
                segment_details["cabin"] = "N/A"
                segment_details["includedCheckedBags"] = 0
                segment_details["includedCabinBags"] = 0
                segment_details["amenities"] = []

            all_segments_info.append(segment_details)
        return all_segments_info