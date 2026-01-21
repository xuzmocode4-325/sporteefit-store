from ninja import Schema
from typing import List



class CartUpdateSchema(Schema):
    product_id: int
    product_qty: int
    action: str

class CartDeleteSchema(Schema):
    product_id: int
    action: str

class CouponApplySchema(Schema):
    coupon_code: str

class CartResponseSchema(Schema):
    cart_qty: int
    product_qty: float

class CartItemSchema(Schema):
    product_id: int
    name: str
    qty: int
    price: float
    slug: str

class CartListResponseSchema(Schema):
    items: List[CartItemSchema]
    cart_qty: int
    total: float