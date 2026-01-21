from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import Order, OrderItem, ShippingAddress
from store.models import Product
from core.utils.tests import get_product, get_user
from django_countries.fields import Country

User = get_user_model()

class OrderModelAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="pass")
        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            shipping_address="123 Street\nCity\nCountry",
            amount_paid=99.99,
            user=self.user
        )

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order - #{self.order.pk}")

    def test_order_creation_and_fields(self):
        self.assertEqual(self.order.full_name, "Test User")
        self.assertEqual(self.order.email, "test@example.com")
        self.assertEqual(float(self.order.amount_paid), 99.99)
        self.assertEqual(self.order.user, self.user)


class OrderItemModelAdminTests(TestCase):
    def setUp(self):
        self.user = get_user()
        self.staff_user = get_user("staff")
        self.int, self.product = get_product(staff_user=self.staff_user)
        self.order = Order.objects.create(
            full_name="Test User", 
            email="test@example.com", 
            shipping_address="123 St",
            amount_paid=49.99
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=49.99,
            user=self.user
        )

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f"Order Item - #{self.order_item.pk}")

    def test_order_item_fields(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(float(self.order_item.price), 49.99)
        self.assertEqual(self.order_item.user, self.user)


class ShippingAddressModelAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user3", email="user3@test.com", password="pass")
        self.address = ShippingAddress.objects.create(
            name="John",
            surname="Doe",
            email="john@example.com",
            address1="123 Elm St",
            address2="Apt 4",
            city="Metropolis",
            state="NY",
            zipcode="12345",
            country="US",  # Use country code as str supported by django_countries
            user=self.user
        )

    def test_shipping_address_str(self):
        self.assertEqual(str(self.address), f"Shipping Address - {self.address.pk}")

    def test_shipping_address_fields(self):
        self.assertEqual(self.address.name, "John")
        self.assertEqual(self.address.surname, "Doe")
        self.assertEqual(self.address.email, "john@example.com")
        self.assertEqual(self.address.address1, "123 Elm St")
        self.assertEqual(self.address.address2, "Apt 4")
        self.assertEqual(self.address.city, "Metropolis")
        self.assertEqual(self.address.state, "NY")
        self.assertEqual(self.address.zipcode, "12345")
        self.assertEqual(self.address.country.code, "US")
        self.assertEqual(self.address.user, self.user)
