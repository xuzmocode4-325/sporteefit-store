from ninja import Router
from django.shortcuts import get_object_or_404
from django_countries import countries

from cart.utils.cart import Cart
from core.schemas import MessageSchema
from django.contrib.auth.models import User


from .models import ShippingAddress, Order, OrderItem
from .schemas import (
    CheckoutResponseSchema, ShippingAddressSchema, 
    CompleteOrderInputSchema
)

router = Router(tags=["Payments"])

@router.get("/checkout", response=CheckoutResponseSchema)
def checkout(request):
    country_choices = list(countries)
    cart = Cart(request)
    shipping_address = None
    if request.user.is_authenticated:
        shipping_address_obj = ShippingAddress.objects.filter(user=request.user.id).first()
        if shipping_address_obj:
            shipping_address = ShippingAddressSchema(
                user_id=shipping_address_obj.user.pk,
                address1=shipping_address_obj.address1,
                address2=shipping_address_obj.address2,
                city=shipping_address_obj.city,
                state=shipping_address_obj.state or "",
                country=str(shipping_address_obj.country) or "",
                zipcode=str(shipping_address_obj.zipcode) or ""
            )
    return {
        "countries": country_choices,
        "cart": list(cart),
        "shipping": shipping_address
    }


@router.post(
    "/complete-order", 
    response={200: MessageSchema, 500: MessageSchema}
)
def complete_order(request, data: CompleteOrderInputSchema):
    full_name = f"{data.fn} {data.sn}"
    shipping_address = "\n".join(filter(
        None, [data.ad1, data.ad2, data.ct, data.st, data.cntry, data.zip])
    )

    cart = Cart(request)
    total_cost = cart.get_total()["discount_total"] if cart.get_total() else 0

    try:
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=full_name,
                email=data.em,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )
        else:
            order = Order.objects.create(
                full_name=full_name,
                email=data.em,
                shipping_address=shipping_address,
                amount_paid=total_cost,
            )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["qty"],
                price=item["price"],
                user=request.user if request.user.is_authenticated else None
            )
        return 200, {"detail": "Order created successfully"}
    except Exception as e:
        # Log the error accordingly
        print(f"Error creating order: {e}")
        return 500, {"detail": "Order creation failed"}