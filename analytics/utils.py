import requests


def fetch_crypto_data(crypto_symbol):

    url = f"https://api.coinbase.com/v2/prices/{crypto_symbol.upper()}-USD/spot"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("data", {})
        return {
            "symbol": data.get("base"),
            "price": float(data.get("amount")),
            "currency": data.get("currency"),
        }

    return None  # Return None if API call fails
