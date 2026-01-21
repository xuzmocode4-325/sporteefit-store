from ninja import Schema
from typing import Optional

class ShippingAddressSchema(Schema):
    user_id: int
    address1: str
    address2: Optional[str] = None
    city: str
    state: str
    country: str
    zipcode: str

class CheckoutResponseSchema(Schema):
    countries: list
    cart: list
    shipping: Optional[ShippingAddressSchema] = None

class CompleteOrderInputSchema(Schema):
    fn: str
    sn: str
    em: str
    ad1: str
    ad2: Optional[str] = None
    ct: str
    st: str
    cntry: str
    zip: str
