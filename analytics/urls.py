from django.urls import path
from .views import CryptoSearchView

urlpatterns = [
    path("search/", CryptoSearchView.as_view(), name="search"),
]
