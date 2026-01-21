from django.test import TestCase
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models import Tag, Category, Product

User = get_user_model()

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Sports", slug="sports")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Sports")
        self.assertEqual(self.tag.slug, "sports")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Sports")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Athleisure", slug="athleisure")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Athleisure")
        self.assertEqual(self.category.slug, "athleisure")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Athleisure")

    def test_category_ordering(self):
        c2 = Category.objects.create(name="Yoga", slug="yoga")
        categories = Category.objects.all()
        # Should be ordered by name alphabetically
        self.assertEqual(list(categories), [self.category, c2])


class ProductModelTest(TestCase):
    def setUp(self):
        self.user_creator = User.objects.create_user(
            username='creator', password='pass', email='creator@mail.com'
        )
        self.user_updater = User.objects.create_user(
            username='updater', password='pass', email='updater@mail.com'
        )
        self.category = Category.objects.create(name="Fitness", slug="fitness")
        # Create a sample product instance
        self.product = Product.objects.create(
            name="Running Shoes",
            brand="FastFeet",
            description="Lightweight running shoes",
            slug="running-shoes",
            price=Decimal('120.00'),
            discount=10,
            category=self.category,
            created_by=self.user_creator,
            updated_by=self.user_updater,
            image='images/products/sample.jpg'  # assuming test env accepts this string
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Running Shoes")
        self.assertEqual(self.product.brand, "FastFeet")
        self.assertEqual(self.product.description, "Lightweight running shoes")
        self.assertEqual(self.product.price, Decimal('120.00'))
        self.assertEqual(self.product.discount, 10)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.created_by, self.user_creator)
        self.assertEqual(self.product.updated_by, self.user_updater)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Running Shoes")

    def test_discount_decimal_conversion(self):
        self.assertEqual(self.product.discount_decimal(), Decimal('0.10'))

    def test_discount_price_calculation(self):
        expected_price = Decimal('120.00') - (Decimal('120.00') * Decimal('0.10'))
        self.assertEqual(self.product.discount_price(), expected_price)

    def test_discount_validator_upper_bound(self):
        self.product.discount = 51
        with self.assertRaises(ValidationError):
            self.product.full_clean()  # triggers model validation

    def test_discount_validator_lower_bound(self):
        self.product.discount = -1
        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_price_max_digits_and_decimal_places(self):
        # max_digits=4 and decimal_places=2 means max 9999.99 price logically
        self.product.price = Decimal('10000.00')
        with self.assertRaises(ValidationError):
            self.product.full_clean()