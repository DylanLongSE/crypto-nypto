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

NY_TZ = pytz.timezone("America/New_York")


def fetch_candlestick_data(crypto_symbol, granularity=3600):
    """
    Fetch candlestick data from Coinbase Pro (time, low, high, open, close, volume),
    convert timestamps to Eastern Time, and return oldest to newest.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)  # last 24 hours

    url = f"{COINBASE_PRO_API}/products/{crypto_symbol}/candles"
    params = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "granularity": granularity,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if not data:
        return None

    data.reverse()

    formatted_data = []
    for row in data:
        candle_time = datetime.utcfromtimestamp(row[0]).replace(tzinfo=pytz.utc)
        eastern_time = candle_time.astimezone(NY_TZ)

        formatted_data.append(
            {
                "timestamp": eastern_time.strftime("%Y-%m-%d %I:%M %p"),
                "open": row[3],
                "high": row[2],
                "low": row[1],
                "close": row[4],
                "volume": row[5],
            }
        )

    return formatted_data
