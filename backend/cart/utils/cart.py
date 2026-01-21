import copy
from decimal import Decimal
from store.models import Product
from django.urls import reverse
from cart.models import Coupon

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key', {})
        self.session['session_key'] = cart  # Ensure session_key is always set
        self.cart = cart
        self.coupon = self.session.get('coupon', None)

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = copy.deepcopy(self.cart)

        for product in products:
            id = str(product.pk)
            cart[id]['product'] = product
            cart[id]['slug'] = product.slug
            cart[id]['discount'] = float(product.discount) if product.discount else 0

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
        
            yield item

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart: 
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'discount': float(product.discount) if product.discount else 0,
                'qty': int(product_qty)
            }
        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product_id:str, product_qty:int):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        self.session.modified = True

    def apply_coupon(self, coupon_code:str):
        try:
            coupon = Coupon.objects.get(name=coupon_code)
            if coupon.discount is not None and coupon.discount >= 0:
                self.coupon = float(coupon.discount)  # Store only the discount value
                self.session['coupon'] = self.coupon  # Store discount in session
            else:
                self.coupon = None
                self.session['coupon'] = None
        except Coupon.DoesNotExist:
            self.coupon = None
            self.session['coupon'] = None
        self.session.modified = True

    def get_total(self):
        total = 0
        savings = 0
        
        for item in self.cart.values():
            price = Decimal(item.get('price', 0))
            discount = Decimal(item.get('discount', 0))

            if discount > 0:
                total += price * item['qty']
                discount_value = price * discount * item['qty'] / 100
                savings += discount_value
            else:
                total += price * item['qty']
                if self.coupon:
                    coupon_discount = Decimal(self.coupon) / 100
                    savings += price * coupon_discount * item['qty']

        discount_total = total - savings

        return {
            'total': float(total),
            'discount_total': float(discount_total),
            'savings': float(savings)
        }