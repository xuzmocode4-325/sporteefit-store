from ninja import Router
from django.http import JsonResponse
from store.models import Product
from cart.utils.cart import Cart 
from .schemas import (
    CartResponseSchema, CartDeleteSchema, 
    CartUpdateSchema, CouponApplySchema, 
    CartItemSchema, CartListResponseSchema
    )

router = Router(tags=['Cart'])

@router.post("/delete", response=CartResponseSchema)
def delete_from_cart(request, data: CartDeleteSchema):
    cart = Cart(request)
    cart.delete(data.product_id)
    return JsonResponse({
        'cart_qty': len(cart),
        'product_qty': float(cart.get_total()['discount_total']),
    })

@router.post("/update", response=CartResponseSchema)
def update_cart(request, data: CartUpdateSchema):
    cart = Cart(request)
    product = Product.objects.filter(id=data.product_id).first()
    if not product:
        return JsonResponse({'detail': 'Product not found'}, status=404)
    cart.add(product, data.product_qty)
    return JsonResponse({
        'cart_qty': len(cart),
        'product_qty': float(cart.get_total()['discount_total']),
    })

@router.post("/apply-coupon")
def apply_coupon(request, data: CouponApplySchema):
    cart = Cart(request)
    cart.apply_coupon(data.coupon_code)

    if cart.coupon:
        return {"success": True}
    else:
        return {"success": False}


@router.get("/items", response=CartListResponseSchema)
def get_cart(request):
    cart = Cart(request)
    items = []
    for item in cart:
        items.append(
            CartItemSchema(
                product_id=item['product'].id,
                name=item['product'].name,
                qty=item['qty'],
                price=float(item['price']),
                slug=item['slug']
            )
        )
    total = float(cart.get_total()['discount_total'])
    return {
        "items": items,
        "cart_qty": len(cart),
        "total": total,
    }
