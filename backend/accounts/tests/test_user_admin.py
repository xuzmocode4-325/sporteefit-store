"""
Test module for django admin modifications.
"""
from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):
    """Test for django admin site."""

    def setUp(self):
        """Log in the admin user before each test."""
        self.client = Client()
        # self.factory = RequestFactory()
        """Create a superuser and a regular user for testing."""
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin-user',
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username='user',
            email='user@example.com',
            password='testcase123',
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:accounts_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:accounts_user_change', args=[self.user.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:accounts_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, HTTPStatus.OK)