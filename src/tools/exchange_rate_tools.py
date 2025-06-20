import requests
from langchain_core.tools import tool
from ..config.clients import BASE_CURRENCY, EXCHANGERATE_BASERURL

@tool
def get_exchange_rate(base_currency: str = BASE_CURRENCY, target_currency: str = None) -> float:
    """
    Fetches the exchange rate from base_currency to target_currency using ExchangeRate API.
    Args:
        base_currency (str): The currency to convert from (e.g., 'USD').
        target_currency (str): The currency to convert to (e.g., 'EUR').
    Returns:
        float: The exchange rate from base_currency to target_currency.
    """
    if not EXCHANGERATE_BASERURL:
        raise ValueError("exchangerate_baseurl is not set. Please check your configuration.")
    response = requests.get(EXCHANGERATE_BASERURL.format(base_currency=base_currency))
    response.raise_for_status()
    data = response.json()
    if 'conversion_rates' in data and target_currency in data['conversion_rates']:
        return data['conversion_rates'][target_currency]
    else:
        raise ValueError(f"Exchange rate for {target_currency} not found in response.")