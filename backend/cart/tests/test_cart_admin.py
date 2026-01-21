"""
Test module for django admin modifications.
"""
from django.urls import reverse
from ..models import Coupon
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
        self.active_coupon = Coupon.objects.create(
            name='active',
            discount=30,
            is_active=True
        )
        self.inactive_coupon = Coupon.objects.create(
            name='inactive',
            discount=30,
            is_active=False
        )

    def test_coupon_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:cart_coupon_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.active_coupon.name)
        self.assertContains(res, self.inactive_coupon.name)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:cart_coupon_change', args=[self.active_coupon.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:cart_coupon_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)