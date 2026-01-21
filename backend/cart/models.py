from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(33)]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {round(self.discount)}% off"