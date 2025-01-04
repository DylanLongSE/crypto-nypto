from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="apple123",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="test_super_user",
            email="test_super_user@gmail.com",
            password="apple345",
        )
        self.assertEqual(admin_user.username, "test_super_user")
        self.assertEqual(admin_user.email, "test_super_user@gmail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
