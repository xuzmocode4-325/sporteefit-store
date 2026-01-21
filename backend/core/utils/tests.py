import random
from store.models import Product, Category
from typing import Optional
from django.contrib.auth import get_user_model

User = get_user_model()
random.seed(144)

def get_user(kind:Optional[str]=None):
    rand_int = random.randint(-1000, 1000)
    if kind == "staff":
        return User.objects.create_user(
            username=f"staff{rand_int}",
            email=f"staff{rand_int}@store.com", 
            password="pass", 
            is_staff=True
        )
    else:  
        return User.objects.create_user(
            username=f"norman{rand_int}",
            email=f"normal{rand_int}@domain.com", 
            password="pass", 
            is_active=True, 
            is_staff=False
        )

def get_product(staff_user, category=None):
    rand_int = random.randint(-1000, 1000)
    if not category:
        category = Category.objects.create(name="Test")
    return rand_int, Product.objects.create(
            name=f"Product{rand_int}",
            brand=f"Brand{rand_int}",
            description=f"Desc{rand_int}",
            slug=f"product{rand_int}",
            price=10.0,
            discount=0,
            category=category,
            created_by=staff_user,
            updated_by=staff_user
        )