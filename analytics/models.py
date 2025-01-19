from django.db import models
from django.conf import settings


class CryptoSearch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user_query = models.CharField(max_length=20)  # BTC, ETH, etc.
    symbol = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")
    timestamp = models.DateTimeField(auto_now_add=True)  # Save when the search happened

    def __str__(self):
        return f"{self.user_query} - {self.symbol} - ${self.price} {self.currency}"
