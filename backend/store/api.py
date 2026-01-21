import logging
from ninja import Router
from typing import List
from .models import Product, Category
from .schemas import ProductSchema, ProductCreateSchema, ProductPatchSchema, CategorySchema
from core.schemas import MessageSchema
from ninja.errors import ValidationError
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


User = get_user_model()
router = Router(tags=["Products"])

@router.get("/categories/", response=List[CategorySchema])
def list_categories(request):
    return Category.objects.all()

@router.get("/products/", response=List[ProductSchema])
def list_products(request):
    return Product.objects.all()

@router.get("/products/{product_id}", response=ProductSchema)
def get_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    return product


@router.post(
    "/products/", auth=django_auth, 
    response={200: ProductSchema, 403: MessageSchema}
)
def create_product(request, data: ProductCreateSchema):
    if not request.user.is_staff:
        return 403, {"detail": "Request not permitted"}
    category = None
    if data.category_id:
        category = get_object_or_404(Category, id=data.category_id)
    product = Product.objects.create(
        name=data.name,
        brand=data.brand or 'unbranded',
        description=data.description or '',
        slug=data.slug,
        price=data.price,
        discount=data.discount or 0,
        category=category,
        created_by=request.user,
        updated_by=request.user
    )
    return product

@router.put(
    "/products/{product_id}", auth=django_auth, 
    response={200: ProductSchema, 403: MessageSchema}
)
def update_product(request, product_id: int, data: ProductPatchSchema):
    if not request.user.is_staff:
        return 403, {"detail": "Request not permitted"}

    product = get_object_or_404(Product, id=product_id)

    # Update simple fields and ForeignKey first
    for attr, value in data.dict(exclude={"tags"}).items():
        if attr == "category":
            setattr(product, attr, get_object_or_404(Category, id=value))
        else:
            setattr(product, attr, value)

    product.updated_by = request.user
    product.save()  # Save before dealing with ManyToMany fields

    # Handle many-to-many fields like tags after saving
    if "tags" in data.dict():
        if data.tags is not None:
            product.tags.set(data.tags)  # Assuming data.tags is a list of IDs
    return product

@router.delete(
    "/products/{product_id}", auth=django_auth, 
    response={200: MessageSchema, 401: MessageSchema, 403: MessageSchema})
def delete_product(request, product_id: int):
        if not request.user.is_staff:
            return 403, {"detail": "Request not permitted"}
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return 200, {"detail": "Item successfully deleted"}