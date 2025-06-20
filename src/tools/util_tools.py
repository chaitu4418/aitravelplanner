from typing import Dict
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from src.config.clients import LLM
from ..models.travel_models import TravelBudgetAllocator
from ..models.enums import BudgetLevel
import datetime

@tool
def calculate_average_time_spent_at_an_address(address: str) -> float:
    """
    Calculates the average time spent by people at a given address.
    Args:
        address (str): The address of the place to estimate time for.
    Returns:
        float: The average time spent in hours.
    """
    prompt = (
        "You are a good time estimator. Please provide me the average time spent by people for '{address}' in a day. "
        "Please provide me a single average time in hours format by extracting from the answer and nothing else. "
        "To this add a buffer time. Only give me the numeric value."
    )
    template = PromptTemplate(
        input_variables=["address"],
        template=prompt
    )
    response = LLM.invoke(template.format(address=address))
    if response and isinstance(response, str):
        try:
            return float(response.strip())
        except ValueError:
            print(f"Could not convert response to float: {response}")
    else:
        print("Invalid response from LLM.")
    return 3.0


@tool
### Convert UNIX to Datetime 
def convert_unix_to_mmddyyyy(timestamp: int) -> str:
    """
    Converts a Unix timestamp (seconds since epoch) to a MM/DD/YYYY string.

    Args:
        timestamp (int): The Unix timestamp to convert.

    Returns:
        str: The formatted date string in MM/DD/YYYY.
    """
    # Convert the Unix timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object to MM/DD/YYYY
    formatted_date = dt_object.strftime("%m/%d/%Y")

    return formatted_date

@tool
### Convert UNIX to Datetime 
def convert_unix_to_yyyymmdd(timestamp: int) -> str:
    """
    Converts a Unix timestamp (seconds since epoch) to a YYYY-MM-DD string.

    Args:
        timestamp (int): The Unix timestamp to convert.

    Returns:
        str: The formatted date string in YYYY-MM-DD.
    """
    # Convert the Unix timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object to YYYY-MM-DD
    formatted_date = dt_object.strftime("%Y-%m-%d")

    return formatted_date


@tool()
def travel_budget_allocator(total_budget: float, trip_type: str, duration_days: int) -> Dict[str, float]:
    """
    Allocates a travel budget across different categories (accommodation, transportation,
    food, activities, miscellaneous) based on the total budget, the desired trip type
    (LOW, MEDIUM, or HIGH), and the duration of the trip in days.

    Returns a dictionary with budget allocation for each category.
    Example: {"accommodation": 700.0, "transportation": 500.0, ...}
    """
    # Instantiate the allocator with the provided arguments
    allocator = TravelBudgetAllocator(total_budget, trip_type, duration_days)
    # Call the allocate method to get the budget breakdown
    return allocator.allocate()