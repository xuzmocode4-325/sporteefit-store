from .models import Coupon
from django.contrib import admin


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'is_active')


admin.site.register(Coupon, CouponAdmin)