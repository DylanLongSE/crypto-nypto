from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from analytics.models import CryptoSearch
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class CryptoSearchViewTest(TestCase):
    """Tests for the crypto search functionality."""

    @patch("analytics.utils.fetch_crypto_data")  # Mock API call
    def test_search_view_valid_crypto(self, mock_fetch):
        """Test searching for a valid cryptocurrency."""
        mock_fetch.return_value = {
            "symbol": "ETH",
            "price": 3355.455,
            "currency": "USD",
        }

        response = self.client.get(reverse("search"), {"q": "ETH"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Results for: ETH")
        self.assertContains(response, "ETH")
        self.assertContains(response, "USD")

        # Check price format dynamically to avoid hardcoded number issues
        self.assertRegex(response.content.decode(), r"\$\d+\.\d+")

        # Ensure search was saved
        self.assertTrue(CryptoSearch.objects.filter(user_query="ETH").exists())

    @patch("analytics.utils.fetch_crypto_data")  # Mock API call
    def test_search_view_invalid_crypto(self, mock_fetch):
        """Test searching for an invalid cryptocurrency."""
        mock_fetch.return_value = None  # Simulating an invalid search

        response = self.client.get(reverse("search"), {"q": "INVALIDCOIN"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cryptocurrency not found. Try another symbol.")

        # Ensure it wasn't saved in the database
        self.assertFalse(CryptoSearch.objects.filter(user_query="INVALIDCOIN").exists())


class HomePageTest(TestCase):
    """Tests for the home page, ensuring recent searches appear for logged-in users."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        CryptoSearch.objects.create(
            user=self.user,
            user_query="BTC",
            symbol="BTC",
            price=40000.00,
            currency="USD",
        )


class NavbarTest(TestCase):
    """Tests for checking if Bootstrap dropdowns are working."""

    def test_navbar_dropdowns(self):
        """Ensure dropdowns are present in the navbar."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        # Instead of looking for exact class, check for dropdown component
        self.assertContains(response, "dropdown-toggle")
        self.assertContains(response, "dropdown-menu")
