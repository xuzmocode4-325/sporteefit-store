"""
Django admin customisation
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserAddress, Profile

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)})
    )
    add_fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
                )
            }
        ),
    )
    readonly_fields = ['last_login']

    def changelist_view(self, request, extra_context=None):
        # Add custom context data if needed
        extra_context = extra_context or {}
        message = "Welcome to the user management panel!"
        extra_context['custom_message'] = message

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(UserAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'city', 'address2', 'address1')
    list_filter = ('country', 'state', 'city')
    search_fields = ('user', 'city', 'address2', 'address1')
    ordering  = ('city',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name',)
    search_fields = ('surname', 'name',)
    ordering  = ('surname', 'name')
    