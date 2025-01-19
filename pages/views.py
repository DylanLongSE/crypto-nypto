from django.views.generic import TemplateView
from django.shortcuts import render
from analytics.models import CryptoSearch


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        recent_searches = (
            CryptoSearch.objects.filter(user=request.user).order_by("-timestamp")[:5]
            if request.user.is_authenticated
            else None
        )

        return render(request, self.template_name, {"recent_searches": recent_searches})


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        recent_searches = (
            CryptoSearch.objects.filter(user=request.user).order_by("-timestamp")[:5]
            if request.user.is_authenticated
            else None
        )

        return render(request, self.template_name, {"recent_searches": recent_searches})
