import requests
from datetime import datetime, timedelta
import pytz


def fetch_crypto_data(crypto_symbol):

    url = f"https://api.coinbase.com/v2/prices/{crypto_symbol.upper()}-USD/spot"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("data", {})
        return {
            "symbol": data.get("base"),
            "current_price": float(data.get("amount")),
            "currency": data.get("currency"),
        }

    return None  # Return None if API call fails


COINBASE_PRO_API = "https://api.exchange.coinbase.com"

# Set timezone based on Django settings
NY_TZ = pytz.timezone("America/New_York")


def fetch_candlestick_data(crypto_symbol, granularity=3600):
    """
    Fetch candlestick (OHLC) data and convert timestamps to Eastern Time (ET).
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)  # Fetch past 24 hours

    url = f"{COINBASE_PRO_API}/products/{crypto_symbol}/candles"
    params = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "granularity": granularity,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        formatted_data = [
            {
                "timestamp": datetime.utcfromtimestamp(c[0])
                .replace(tzinfo=pytz.utc)
                .astimezone(NY_TZ)
                .strftime("%Y-%m-%d %I:%M %p"),
                "open": c[1],
                "high": c[2],
                "low": c[3],
                "close": c[4],
                "volume": c[5],
            }
            for c in data
        ]
        return formatted_data

    return None  # Return None if API request fails
