import os
import uuid
from functools import partial
from django.db import models
from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


def model_image_file_path(instance, filename, model=None):
    """
    Generate file path for uploaded images.
    The filename becomes a UUID to avoid collisions.

    Example:
        uploads/profile/uuid4.png
    """
    ext = os.path.splitext(filename)[1]  # e.g. '.png'
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", model, filename)


class UserManager(BaseUserManager):
    """Class for creating a user manager"""

    def create_user(self, username, email, password=None, **extrafields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError(
                'An email address is required for user registration.'
            )
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Model for custom definition of system user fields"""
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.AutoField
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def _str_(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=partial(model_image_file_path, model="profile")
    )

    def __str__(self):
        return  f"{self.name} {self.surname}"
    
class UserAddress(models.Model):
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True, blank_label="(Select Country)")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        return  f"{self.address1} {self.address2}"