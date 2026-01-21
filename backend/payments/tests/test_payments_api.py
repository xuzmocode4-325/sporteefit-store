import json
from http import HTTPStatus
from django.test import TestCase, Client
from ninja.testing import TestClient
from django.contrib.auth import get_user_model
from payments.api import router  # Adjust import to your actual api router module
from payments.models import ShippingAddress, Order, OrderItem
from store.models import Product
from django_countries import countries
from core.utils.tests import get_user, get_product

User = get_user_model()
client = TestClient(router)

class PaymentsApiTests(TestCase):
    def setUp(self):
        self.session_client = Client()
        self.user = get_user()
        self.int, self.product = get_product(
            staff_user=get_user("staff")
        )

    def test_checkout_anonymous(self):
        response = self.session_client.get("/api/payments/checkout")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_countries = [list(c) for c in countries]
        self.assertListEqual(data["countries"], expected_countries)
        self.assertIsInstance(data["cart"], list)
        self.assertIsNone(data["shipping"])

    def test_checkout_authenticated_with_shipping(self):
        ShippingAddress.objects.create(
            user=self.user,
            name="John",
            surname="Doe",
            email="john@example.com",
            address1="123 Street",
            city="City",
            state="State",
            country="US",
            zipcode="1234"
        )
        self.session_client.force_login(user=self.user)
        response = self.session_client.get("/api/payments/checkout")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn("shipping", data)
        self.assertEqual(data["shipping"]["user_id"], self.user.pk)

    def test_complete_order_success_authenticated(self):
        payload = {
            "fn": "John",
            "sn": "Doe",
            "em": "john@example.com",
            "ad1": "123 Street",
            "ad2": "",
            "ct": "City",
            "st": "State",
            "cntry": "US",
            "zip": "12345"
        }
        self.session_client.force_login(user=self.user)
        response = self.session_client.post(
            "/api/payments/complete-order", 
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["detail"], "Order created successfully")

    def test_complete_order_success_anonymous(self):
        payload = {
            "fn": "Jane",
            "sn": "Smith",
            "em": "jane@example.com",
            "ad1": "456 Road",
            "ad2": "Suite 1",
            "ct": "Town",
            "st": "Province",
            "cntry": "CA",
            "zip": "98765"
        }
        response = self.session_client.post(
            "/api/payments/complete-order", 
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Order created successfully")
