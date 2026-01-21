"""
Module for testing any models within the core app.
"""
from decimal import Decimal
from django.test import TestCase
from .. import models


class ModelTests(TestCase):
    def test_create_coupon(self):
        "Test creating a coupon is successful"

        name = "Black Friday Special"
        discount = 10.00

        coupon = models.Coupon.objects.create(
            name=name,
            discount=Decimal(discount),
            is_active=True
        )
        
        self.assertEqual(str(coupon), f"{name} - {round(discount)}% off")