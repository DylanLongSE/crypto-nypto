from django.views.generic import TemplateView
from django.shortcuts import render
from .models import CryptoSearch
from .utils import fetch_crypto_data


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
                    price=crypto_data.get("price"),
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
