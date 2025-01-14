from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    # Set email as the primary identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Keep username as a required field

    def __str__(self):
        return self.username
