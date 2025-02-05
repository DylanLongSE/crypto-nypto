from django.views.generic import TemplateView
from django.shortcuts import render
from analytics.models import CryptoSearch
from analytics.utils import fetch_valid_coins


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            recent_searches = CryptoSearch.objects.filter(user=request.user).order_by(
                "-timestamp"
            )[:5]
            coin_symbols = fetch_valid_coins()
            context["recent_searches"] = recent_searches
            context["coin_symbols"] = coin_symbols
        return render(request, self.template_name, context)
