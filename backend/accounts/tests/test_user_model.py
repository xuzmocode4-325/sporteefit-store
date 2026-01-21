from django.test import TestCase
from django.contrib.auth import get_user_model

def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email, password)


class UserModelTests(TestCase):
    """
    Class for testing user model.
    """

    def test_create_user_with_email_success(self):
        """Test for successful creation of user with email address."""
        username = 'user'
        email = 'test@example.com'
        password = 'test@123'
        user = get_user_model().objects.create_user(
            username,
            email,
            password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_mormalized(self):
        """Test email mormalization for new users."""
        username = 'user'
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
            ['Test5@Example.Com', 'Test5@example.com']
        ]

        for num, (email, expected) in enumerate(sample_emails):
            user = get_user_model().objects.create_user(
                username=f"{username}_{num}",
                email=email, 
                password='sample123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a new user without an email raises a value error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username='test', email="", password='test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'user',
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)