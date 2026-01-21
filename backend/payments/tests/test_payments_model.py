from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import Order, OrderItem, ShippingAddress
from store.models import Product
from django.core.exceptions import ValidationError
from core.utils.tests import get_user, get_product

User = get_user_model()


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = get_user()

    def test_create_order_success(self):
        order = Order.objects.create(
            full_name="John Doe",
            email="john@example.com",
            shipping_address="123 Test St\nCity\nCountry",
            amount_paid=100.00,
            user=self.user
        )
        self.assertEqual(order.full_name, "John Doe")
        self.assertEqual(order.email, "john@example.com")
        self.assertEqual(float(order.amount_paid), 100.00)
        self.assertEqual(order.user, self.user)

    def test_str_method(self):
        order = Order.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            shipping_address="456 Test Ave",
            amount_paid=200.00
        )
        self.assertEqual(str(order), f"Order - #{order.pk}")

class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = get_user()
        self.int, self.product = get_product(
            staff_user=get_user("staff")
        )
        self.order = Order.objects.create(
            full_name="John Smith",
            email="johnsmith@example.com",
            shipping_address="789 Road",
            amount_paid=50.00
        )

    def test_create_order_item_success(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=30.00,
            user=self.user
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(float(order_item.price), 30.00)
        self.assertEqual(order_item.user, self.user)

    def test_str_method(self):
        address = ShippingAddress.objects.create(
            name="Bob",
            surname="Jones",
            email="bob@example.com",
            address1="456 Elm St",
            city="Shelbyville",
            country="US"
        )
        self.assertEqual(str(address), f"Shipping Address - {address.pk}")