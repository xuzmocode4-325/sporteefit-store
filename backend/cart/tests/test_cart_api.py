
from core.utils.tests import get_product, get_user
from ninja.testing import TestClient
from store.models import Product, Category
from cart.models import Coupon
from cart.api import router  
from http import HTTPStatus
from django.test import TestCase, Client

client = TestClient(router)

class CartApiTests(TestCase):
    def setUp(self):
        self.session_client = Client()
        self.staff_user = get_user("staff")
        self.category = Category.objects.create()
        # Create sample products
        self.int1, self.product1 = get_product(self.staff_user, self.category)
        self.int2, self.product2 = get_product(self.staff_user, self.category)
        # Create a valid coupon
        self.coupon = Coupon.objects.create(name="DISCOUNT10", discount=10)

    def test_add_update_cart(self):
        # Add product1 quantity 2
        res = self.session_client.post(
            "/api/cart/update", 
            content_type="application/json",
            data={
                "product_id": self.product1.pk,
                "product_qty": 2,
                "action": "post"
            }
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()['cart_qty'], 2)

        # Update product1 quantity to 3
        res = self.session_client.post(
            "/api/cart/update", 
            content_type="application/json",
            data={
                "product_id": self.product1.pk,
                "product_qty": 3,
                "action": "post"
            }
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()['cart_qty'], 3)

    def test_delete_from_cart(self):
        # First add a product
        self.session_client.post(
            "/api/cart/update", 
            content_type="application/json",                  
            data={
                "product_id": self.product1.pk,
                "product_qty": 1,
                "action": "post"
            }
        )

        # Delete product1 from cart
        res = self.session_client.post(
            "/api/cart/delete", 
            content_type="application/json",                   
            data={
                "product_id": self.product1.pk,
                "action": "post"
            }
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()['cart_qty'], 0)

    def test_apply_valid_coupon(self):
        res =self.session_client.post(
            "/api/cart/apply-coupon",
            content_type="application/json", 
            data={
                "coupon_code": self.coupon.name
            }
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTrue(res.json()['success'])

    def test_apply_invalid_coupon(self):
        res =self.session_client.post(
            "/api/cart/apply-coupon",
            content_type="application/json", 
            data={
                "coupon_code": "INVALIDCODE"
            }
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertFalse(res.json()['success'])

    def test_get_cart_empty(self):
        res = self.session_client.get("/api/cart/items")
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data['cart_qty'], 0)
        self.assertEqual(data['items'], [])
        self.assertEqual(data['total'], 0)

    def test_get_cart_with_items(self):
        # Add two products
        self.session_client.post("/api/cart/update",
            content_type="application/json", 
            data={
                "product_id": self.product1.pk,
                "product_qty": 2,
                "action": "post"
            }
        )
        self.session_client.post("/api/cart/update",
            content_type="application/json", 
            data={
                "product_id": self.product2.pk,
                "product_qty": 1,
                "action": "post"
            }
        )

        res = self.session_client.get("/api/cart/items")
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data['cart_qty'], 3)
        self.assertEqual(len(data['items']), 2)
        ids = [item['product_id'] for item in data['items']]
        self.assertIn(self.product1.pk, ids)
        self.assertIn(self.product2.pk, ids)
        # Check quantities
        qty_map = {item['product_id']: item['qty'] for item in data['items']}
        self.assertEqual(qty_map[self.product1.pk], 2)
        self.assertEqual(qty_map[self.product2.pk], 1)
