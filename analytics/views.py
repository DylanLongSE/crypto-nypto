from django.views.generic import TemplateView
from django.shortcuts import render
from .models import CryptoSearch
from .utils import fetch_crypto_data, fetch_candlestick_data, fetch_valid_coins
import plotly.graph_objects as go
from plotly.offline import plot
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class CryptoSearchView(LoginRequiredMixin, TemplateView):
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

        coin_symbols = fetch_valid_coins()

        context = {
            "crypto": crypto_data,
            "error": error_message,
            "query": query,
            "recent_searches": recent_searches,
            "coin_symbols": coin_symbols,
        }

        return render(request, self.template_name, context)


@login_required
def candlestick_chart_view(request, symbol="BTC-USD"):
    granularity = request.GET.get("granularity", "3600")  # Default to 3600
    try:
        granularity = int(granularity)
    except ValueError:
        granularity = "3600"

    candlestick_data = fetch_candlestick_data(symbol, int(granularity))

    if not candlestick_data:
        return render(
            request,
            "candlestick_chart.html",
            {
                "symbol": symbol,
                "granularity": granularity,
                "candlestick_chart": "<p>No data available</p>",
            },
        )

    # Process data and generate chart
    timestamps = [item["timestamp"] for item in candlestick_data]
    opens = [item["open"] for item in candlestick_data]
    highs = [item["high"] for item in candlestick_data]
    lows = [item["low"] for item in candlestick_data]
    closes = [item["close"] for item in candlestick_data]

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=timestamps,
                open=opens,
                high=highs,
                low=lows,
                close=closes,
                increasing=dict(line=dict(color="green")),
                decreasing=dict(line=dict(color="red")),
            )
        ]
    )

    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        xaxis_title="Time",
        yaxis=dict(
            title="Price (USD)",
            tickprefix="$",
            title_standoff=20,
        ),
        xaxis=dict(
            tickangle=-45,
            tickmode="auto",
            nticks=20,
            tickformat="%b %d, %I:%M %p",
            rangeslider_visible=False,
        ),
        template="seaborn",
    )

    candlestick_chart = plot(fig, output_type="div")

    return render(
        request,
        "candlestick_chart.html",
        {
            "symbol": symbol,
            "granularity": granularity,
            "candlestick_chart": candlestick_chart,
        },
    )
