from decimal import Decimal
from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    brand= models.CharField(max_length=250, default='unbranded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/products')
    discount = models.SmallIntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(33)])
    category = models.ForeignKey(
        Category, related_name='product', 
        on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='product', on_delete=models.DO_NOTHING
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='modified_product',
        null=True
    )
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    
    def discount_decimal(self):
        """Convert discount percentage to a decimal."""
        return Decimal(self.discount) / Decimal(100)
    
    def discount_price(self):
        return Decimal(self.price) - (
            Decimal(self.price)  *  
            Decimal(self.discount) / Decimal(100)
        )