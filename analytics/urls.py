from django.urls import path
from .views import CryptoSearchView, candlestick_chart_view

urlpatterns = [
    path("search/", CryptoSearchView.as_view(), name="search"),
    path(
        "chart/<str:symbol>/<int:granularity>/",
        candlestick_chart_view,
        name="crypto-chart",
    ),
]
