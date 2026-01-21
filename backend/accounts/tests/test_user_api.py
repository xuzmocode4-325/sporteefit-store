import io
import os
import json
import http
import tempfile
from PIL import Image
from http import HTTPStatus
from django.test import (
    TestCase, Client, RequestFactory, override_settings
)
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from ninja.testing import TestClient
from unittest.mock import MagicMock, patch

from accounts.api import router  
from accounts.utils.emails import send_verification_email
from accounts.models import Profile, model_image_file_path

User = get_user_model()
client = TestClient(router)

def create_user(**params):
    """Helper to create a user for tests."""
    return User.objects.create_user(**params)


class TestUnverifiedRequests(TestCase):
    def setUp(self):
        self.session_client = Client()
        self.credentials = {
            "username": "unverified",
            "email": "uv@example.com",
            "password": "strongpass123",
        }
        self.user = create_user(**self.credentials)

    @patch("accounts.api.send_verification_email", return_value=True)
    def test_successful_registration(self, mock_send_email): # error
        payload = {
            "username": "example-user",
            "email": "example-user@test.com",
            "password": "pass12345",
        }
        res = client.post("/register", json=payload)
        self.assertEqual(res.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(res.json().get("detail"), "User created and email verification sent")

        user = User.objects.get(email=self.credentials["email"])
        self.assertFalse(user.is_active)
        mock_send_email.assert_called_once()

    @patch("accounts.api.send_verification_email", return_value=False)
    def test_registration_email_fail(self, mock_send_email):
        res = client.post("/register", self.credentials)

        self.assertEqual(res.status_code, http.HTTPStatus.UNPROCESSABLE_ENTITY)

        user = User.objects.get(email=self.credentials["email"])
        user_filter = User.objects.filter(email=self.credentials["email"])
        self.assertTrue(user_filter.exists())
        self.assertFalse(user.is_active)

    def test_registration_missing_field(self):
        invalid_payload = {"username": "testuser"}
        res = client.post("/register", invalid_payload)

        self.assertEqual(res.status_code, http.HTTPStatus.UNPROCESSABLE_ENTITY)
        data = res.json()
        self.assertNotIn("email", str(data))
        self.assertNotIn("password", str(data))

    def test_register_duplicate_email_error(self):
        payload = {
            "username": "spoof-user",
            "email": self.credentials["email"],
            "password": "passt-12345",
        }
        res = client.post("/register", json=payload)
        self.assertIn(
            res.status_code, (
            http.HTTPStatus.UNPROCESSABLE_ENTITY, 
            http.HTTPStatus.INTERNAL_SERVER_ERROR
            )
        )

    def test_register_duplicate_username_error(self): 
        payload = {
            "username": self.credentials["username"],
            "email": "random@spoofmail.com",
            "password": "passt-12345",
        }
        res = client.post("/register", json=payload)
        self.assertIn(
            res.status_code, (
            http.HTTPStatus.UNPROCESSABLE_ENTITY, 
            http.HTTPStatus.INTERNAL_SERVER_ERROR
            )
        )

    def test_login_fail_with_username(self): # fail
        session_client = Client()
        payload = {"username": self.credentials["username"], "password": self.credentials["password"]}
        res = session_client.post(
            "/api/accounts/login",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, http.HTTPStatus.UNAUTHORIZED)
        self.assertIn(res.json().get("detail"), 
            ("Invalid credentials.", "Account is inactive.")
        )

    def test_login_fail_with_email(self):
        session_client = Client()
        payload = {"email": self.credentials["email"], "password": self.credentials["password"]}

        res = session_client.post(
            "/api/accounts/login",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, http.HTTPStatus.UNAUTHORIZED)
        self.assertIn(res.json().get("detail"), 
            ("Invalid credentials.", "Account is inactive.")
        )


class SendVerificationEmailTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # You might want to use a custom user creation if you have a custom User model
        self.user = create_user(
            username='testuser', 
            email='test@example.com', 
            password='secret'
        )
        self.request = self.factory.get('/')
        self.request.user = self.user

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_is_sent(self):
        # Calling the utility should result in one email in the outbox
        send_verification_email(self.request, self.user)
        self.assertEqual(len(mail.outbox), 1)
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_subject_and_recipient(self):
        send_verification_email(self.request, self.user)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user.email])
        self.assertIn("Welcome to", email.subject)
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_body_contains_username_and_domain(self):
        send_verification_email(self.request, self.user)
        email = mail.outbox[0]
        self.assertIn(self.user.username, email.body)
        # Depending on how get_current_site works in your environment,
        # you may need to check for the test server's domain or similar.
      
        domain = get_current_site(self.request).domain
        self.assertIn(domain, email.body)
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('accounts.utils.emails.render_to_string')
    def test_email_template_context(self, mock_render_to_string):
        # Ensure the right context values are passed to the template
        mock_render_to_string.return_value = "<p>dummy</p>"
        send_verification_email(self.request, self.user)
        context, _ = mock_render_to_string.call_args[0][1], mock_render_to_string.call_args[1]
        self.assertEqual(context['username'], self.user.username)
        self.assertIn('uid', context)
        self.assertIn('token', context)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('accounts.utils.emails.EmailMessage.send')
    def test_email_send_called_once(self, mock_send):
        # Ensures EmailMessage.send is called once (side-effect not repeated)
        send_verification_email(self.request, self.user)
        mock_send.assert_called_once()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_is_html(self):
        send_verification_email(self.request, self.user)
        email = mail.outbox[0]
        self.assertEqual(email.content_subtype, "html")


class TestVerifiedRequests(TestCase):
    """Test public endpoints like register and login."""

    def setUp(self):
        self.session_client = Client()
        self.credentials = {
            "username": "authuser",
            "email": "auth@example.com",
            "password": "strongpass123",
            "is_active": True
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_login_invalid_credentials(self): 
        payload = {"username": "loginuser", "password": "badpass"}
        res = client.post("/login", json=payload)
        self.assertEqual(res.status_code, http.HTTPStatus.UNAUTHORIZED)
        self.assertEqual(res.json().get("detail"), "Invalid credentials.")

    def test_login_success_with_username(self): 
        payload = {"username": self.credentials["username"], "password": self.credentials["password"]}
        res = self.session_client.post(
            "/api/accounts/login",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertIn(res.status_code, (http.HTTPStatus.OK, http.HTTPStatus.OK))
        self.assertEqual(res.json().get("detail"), "Login successful.")

    def test_login_success_with_email(self):
        payload = {"email": self.credentials["email"], "password": self.credentials["password"]}

        res = self.session_client.post(
            "/api/accounts/login",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertIn(res.status_code, (http.HTTPStatus.OK, http.HTTPStatus.OK))
        self.assertEqual(res.json().get("detail"), "Login successful.")

    def test_csrf_token_endpoint(self):
        res = client.get("/set-csrf-token")
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        self.assertIn("detail", res.json())

class TestAuthenticatedRequests(TestCase):
    """Test endpoints that require authentication (login session)."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="dummy",
            email="dummy@example.com",
            password="testpass123"
        )

    def test_get_profile_success(self):
        res = client.get("/profile", user=self.user)
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        self.assertEqual(res.json().get("username"), self.user.username)
        self.assertEqual(res.json().get("email"), self.user.email)

    def test_update_profile(self):
        payload = {"name": "Updated", "surname": "User"}
        res = client.patch("/profile", data=payload, user=self.user)
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        self.assertEqual(res.json().get("name"), "Updated")

    def test_delete_account(self):
        res = client.delete("/profile", user=self.user)
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        self.assertEqual(res.json().get("detail"), "User account deleted successfully.")
        self.assertFalse(User.objects.filter(id=self.user.pk).exists())

class TestAuthenticatedAdminRequests(TestCase):
    """Test superadmin functionality for user management."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass"
        )
        self.regular_user = User.objects.create_user(
            username="reguser", email="reg@example.com", password="regpass"
        )

    def test_admin_create_user(self):  
        payload = {
            "username": "createdbyadmin",
            "email": "new@example.com",
            "password": "newpass123",
            "name": "New",
            "surname": "User",
            "is_active": True,
            "is_staff": False
        }
        res = client.post("/users", json=payload, user=self.superuser)
        self.assertEqual(res.status_code, http.HTTPStatus.CREATED)
        result = res.json()
        self.assertEqual(result["username"], "createdbyadmin")
        self.assertEqual(result["email"], "new@example.com")

    def test_admin_update_user(self):
        user = create_user(username="moduser", email="mod@example.com", password="pass")
        payload = {"email": "updated@example.com", "is_active": False}
        res = client.patch(f"/users/{user.pk}", json=payload, user=self.superuser)
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.email, payload["email"])
        self.assertFalse(updated_user.is_active)

    def test_admin_delete_user(self):
        user = create_user(username="deleteuser", email="del@example.com", password="pass")
        res = client.delete(f"/users/{user.pk}", user=self.superuser)
        self.assertEqual(res.status_code, http.HTTPStatus.OK)
        self.assertEqual(res.json().get("detail"), "User deleted successfully.")
        exists = User.objects.filter(pk=user.pk).exists()
        self.assertFalse(exists)

    # Negative tests: admin endpoints by non-admin
    def test_non_admin_create_user_forbidden(self): 
        payload = {
            "username": "shouldfail",
            "email": "fail@example.com",
            "password": "failpass",
            "name": "Fail",
            "surname": "User",
            "is_active": True,
            "is_staff": False
        }
        res = client.post("/users", json=payload, user=self.regular_user)
        self.assertIn(res.status_code, (http.HTTPStatus.FORBIDDEN, http.HTTPStatus.UNAUTHORIZED))

    def test_non_admin_update_user_forbidden(self): 
        user = create_user(username="targetuser", email="target@example.com", password="pass")
        payload = {"email": "hack@example.com", "is_active": False}
        res = client.patch(f"/users/{user.pk}", json=payload, user=self.regular_user)
        self.assertIn(res.status_code, (http.HTTPStatus.FORBIDDEN, http.HTTPStatus.UNAUTHORIZED))

    def test_non_admin_delete_user_forbidden(self): 
        user = create_user(username="targetuser2", email="target2@example.com", password="pass")
        res = client.delete(f"/users/{user.pk}", user=self.regular_user)
        self.assertIn(res.status_code, (http.HTTPStatus.FORBIDDEN, http.HTTPStatus.UNAUTHORIZED))


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TestProfileImageUpload(TestCase):
    def setUp(self):
        """
        Create an active test user and associated profile.
        """
        self.user = User.objects.create_user(
            username="imguser",
            email="img@example.com",
            password="testpass123",
            is_active=True,
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def generate_temp_image(self, name="avatar.png"):
        """
        Generate an in-memory temporary image for upload.
        """
        file = io.BytesIO()
        image = Image.new("RGB", (200, 200), color="white")
        image.save(file, format="PNG")
        file.name = name
        file.seek(0)
        return file

    @patch("accounts.models.uuid.uuid4")
    def test_profile_file_name_uuid(self, mock_uuid):
        """
        Ensure the file name is generated using a UUID.
        """
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = model_image_file_path(instance=None, model="profile", filename="example.jpg")
        expected_path = f"uploads/profile/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)

    def test_upload_profile_image(self):
        """
        Uploads a valid image and ensures it is saved to storage correctly.
        """
        image_file = self.generate_temp_image()

        image = SimpleUploadedFile(
            name=image_file.name,
            content=image_file.read(),
            content_type="image/png",
        )

        # Perform multipart/form-data upload request
        res = self.client.post(
            "/api/accounts/upload-profile-image",
            data={"image": image},
            format="multipart",
        )

        self.assertEqual(res.status_code, HTTPStatus.OK, msg=res.content)
        data = res.json()
        self.assertIn("detail", data)
        self.assertIn("image", data)

        # Refresh profile from DB to check if file persisted
        profile = Profile.objects.get(user=self.user)
        normalized_path = os.path.normpath(profile.image.name)

        self.assertIn(os.path.join("uploads", "profile"), normalized_path)
        self.assertTrue(normalized_path.endswith(".png"))
        self.assertNotIn("avatar.png", profile.image.name)
        self.assertEqual(data["detail"], "Profile image uploaded successfully.")
