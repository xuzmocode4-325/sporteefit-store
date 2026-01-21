from .models import Product, Category
from ninja import ModelSchema
from typing import Optional
from decimal import Decimal


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSchema(ModelSchema):
    price: Optional[float]
    discount: Optional[int]
    class Meta: 
        model = Product
        fields = ['id', 'name', 'brand', 'description', 'slug', 'category']

class ProductCreateSchema(ModelSchema):
    category_id: int
    discount: int
    price: float
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'slug']

class ProductPatchSchema(ModelSchema):
    class Meta: 
        model = Product
        fields = "__all__"
        fields_optional = '__all__'
        exclude = ["created_by", "updated_by"]
