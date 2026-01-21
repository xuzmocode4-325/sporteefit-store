import json
import random
from http import HTTPStatus
from typing import Optional
from django.test import TestCase, Client
from ninja.testing import TestClient
from ..api import router  # Assuming the router is in api.py in the same app
from ..models import Product, Category
from core.utils.tests import get_user, get_product 


client = TestClient(router)


class TestUnauthenticatedProductRequests(TestCase):
    def setUp(self):
        self.staff_user = get_user("staff")
        self.session_client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.int1, self.prod1 = get_product(self.staff_user, self.category)
        self.int2, self.prod2 = get_product(self.staff_user, self.category)

    def test_list_products(self):
        res = client.get("/products/")
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.json()), 2)
        names = [prod['name'] for prod in res.json()]
        self.assertIn(f"Product{self.int1}", names)
        self.assertIn(f"Product{self.int2}", names)

    def test_get_product_success(self):
        res = client.get(f"/products/{self.prod1.pk}")
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()['name'], f"Product{self.int1}")

    def test_get_product_not_found(self):
        res = client.get("/products/9999")  # Non-existent ID
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_product_unauthorised(self): # fails
        res = client.delete(
            f"/products/{self.prod1.pk}",
            content_type="application/json"
        )
        self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(res.json()['detail'], "Unauthorized")

    def test_create_product_unauthorized(self):
        # Without auth, should fail
        data = {
            "name": "NewProduct",
            "slug": "new-product",
            "price": 30.0,
            "category_id": self.category.pk
        }
        res = client.post(
            "/products/", 
            json=data,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED) 

class TestAuthenticatedProductRequests(TestCase):
    def setUp(self):
        # Create categories
        self.category = Category.objects.create(name="Electronics")

        # Create users
        self.user = get_user()
        self.staff_user = get_user("staff")

        # Create some products
        self.product1 = Product.objects.create(
            name="Product1",
            brand="BrandA",
            description="Desc1",
            slug="product1",
            price=10.0,
            discount=0,
            category=self.category,
            created_by=self.staff_user,
            updated_by=self.staff_user
        )

        self.product2 = Product.objects.create(
            name="Product2",
            brand="BrandB",
            description="Desc2",
            slug="product2",
            price=20.0,
            discount=5,
            created_by=self.staff_user,
            updated_by=self.staff_user
        )

        self.product_data = data = {
            "name": "NewProduct",
            "slug": "new-product",
            "price": 30.0,
            "category_id": self.category.pk,
            "brand": "BrandX",
            "description": "DescriptionX",
            "discount": 10
        }

        # Initialize TestClient with the router
        self.session_client = Client(router)
        self.session_client.force_login(user=self.staff_user)

    def test_create_product_success(self):
        res = client.post(
            "/products/", 
            json=self.product_data, 
            content_type="application/json", 
            user=self.staff_user
        )
        self.assertEqual(res.status_code, 200)
        product_data = res.json()
        self.assertEqual(product_data['name'], "NewProduct")
        self.assertEqual(product_data['brand'], "BrandX")
        self.assertEqual(product_data['discount'], 10)
        self.assertEqual(product_data['category'], self.category.pk)

    def test_update_product_success(self):
        data = {
            "name": "Updated Name",
            "slug": "updated-name",
            "price": 99.90,
            "brand": "Updated Brand",
            "description": "Updated Description",
            "discount": 15,
            "category_id": self.category.pk
        }
        res = client.put(
            f"/products/{self.product1.pk}", 
            json=data,
            content_type="application/json",
            user=self.staff_user
        )
        self.assertEqual(res.status_code, 200)
        product_data = res.json()
        self.assertEqual(product_data['name'], "Updated Name")
        self.assertEqual(product_data['slug'], "updated-name")
        self.assertEqual(product_data['price'], 99.90)
        self.assertEqual(product_data['brand'], "Updated Brand")
        self.assertEqual(product_data['description'], "Updated Description")
        self.assertEqual(product_data['discount'], 15)
   
    def test_delete_product_success(self):
        res = client.delete(
            f"/products/{self.product1.pk}",
            content_type="application/json",
            user=self.staff_user
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()['detail'], "Item successfully deleted")
        exists = Product.objects.filter(pk=self.product1.pk).exists()
        self.assertFalse(exists)


    def test_delete_product_not_found(self):
        res = client.delete(
            "/products/9999",
            content_type="application/json",
            user=self.staff_user
        )
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)


    def test_update_product_not_found(self):
        data = {
            "name": "UpdatedName",
            "slug": "updated-slug",
            "price": 99.9
        }
        res = client.put(
            "/products/9999", 
            json=data, 
            content_type="application/json",
            user=self.staff_user
        )
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(res.json()["detail"], "Not Found")

    def test_create_product_forbidden_non_staff(self):
        res = client.post(
            "/products/", 
            json=self.product_data, 
            content_type="application/json", 
            user = self.user
        )
        self.assertEqual(res.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(res.json()["detail"], "Request not permitted")


    def test_update_product_forbidden_non_staff(self):
        data = {
            "name": "UpdatedName",
            "slug": "updated-slug",
            "price": 99.9
        }

        res = client.put(
            f"/products/{self.product1.pk}",
            json=data, 
            user=self.user
        )
        self.assertEqual(res.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(res.json()["detail"], "Request not permitted")

    def test_delete_product_forbidden_non_staff(self):
        data = {
            "name": "UpdatedName",
            "slug": "updated-slug",
            "price": 99.9
        }

        res = client.delete(
            f"/products/{self.product1.pk}",
            json=data, 
            user=self.user
        )
        self.assertNotEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(res.json()["detail"], "Request not permitted")


    