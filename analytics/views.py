from django.views.generic import TemplateView
from django.shortcuts import render
from .utils import fetch_crypto_data


class CryptoSearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").upper()  # Get crypto symbol from URL parameter
        crypto_data = None
        error_message = None

        if query:
            crypto_data = fetch_crypto_data(query)
            if not crypto_data:
                error_message = "Cryptocurrency not found. Try another symbol."

        context = {"crypto": crypto_data, "error": error_message, "query": query}
        return render(request, self.template_name, context)
