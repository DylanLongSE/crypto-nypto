from django.contrib import admin
from .models import CryptoSearch


@admin.register(CryptoSearch)
class CryptoSearchAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "user_query",
        "symbol",
        "current_price",
        "currency",
        "timestamp",
    )
    search_fields = ("user_query", "symbol")
    list_filter = ("currency", "timestamp")
