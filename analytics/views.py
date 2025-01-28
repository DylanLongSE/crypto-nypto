from django.views.generic import TemplateView
from django.shortcuts import render
from .models import CryptoSearch
from .utils import fetch_crypto_data, fetch_candlestick_data
import plotly.graph_objects as go
from plotly.offline import plot


class CryptoSearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").upper()  # Get crypto symbol from URL parameter
        crypto_data = None
        error_message = None

        if query:  # if 'query' is not empty
            crypto_data = fetch_crypto_data(query)  # fetch_crypto_data in utils.py

            # if fetch_crypto_data returned None (couldn't find in api)
            if not crypto_data:
                error_message = "Cryptocurrency not found. Try another symbol."
            else:
                CryptoSearch.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    user_query=query,
                    symbol=crypto_data.get("symbol"),
                    current_price=crypto_data.get("current_price"),
                    currency=crypto_data.get("currency", "USD"),
                )

        recent_searches = (
            CryptoSearch.objects.filter(user=request.user).order_by("-timestamp")[:5]
            if request.user.is_authenticated
            else None
        )

        context = {
            "crypto": crypto_data,
            "error": error_message,
            "query": query,
            "recent_searches": recent_searches,
        }

        return render(request, self.template_name, context)


def candlestick_chart_view(request, symbol="BTC-USD", granularity=3600):
    """
    Django view to generate a candlestick chart using Plotly.
    """
    candlestick_data = fetch_candlestick_data(symbol, granularity)

    if candlestick_data:
        timestamps = [item["timestamp"] for item in candlestick_data]
        opens = [item["open"] for item in candlestick_data]
        highs = [item["high"] for item in candlestick_data]
        lows = [item["low"] for item in candlestick_data]
        closes = [item["close"] for item in candlestick_data]

        # Create a Plotly Candlestick Chart
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=timestamps,
                    open=opens,
                    high=highs,
                    low=lows,
                    close=closes,
                    name=symbol,
                )
            ]
        )

        fig.update_layout(
            title=f"{symbol} Candlestick Chart",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
        )

        # Convert figure to HTML
        candlestick_chart = plot(fig, output_type="div")

    else:
        candlestick_chart = "<p>No data available</p>"

    context = {
        "symbol": symbol,
        "candlestick_chart": candlestick_chart,
    }

    return render(request, "candlestick_chart.html", context)
