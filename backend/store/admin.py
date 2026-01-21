from django.contrib import admin
from .models import Category, Product, Tag

# # Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by', 'created_at')
    prepopulated_fields = {'slug':('name',)}
    readonly_fields = ['created_by', 'created_at', 'updated_by']
    list_display = ('name',)
    search_fields = ('name',)
    def save_model(self, request, obj, form, change):
            """Override save_model to set created_by to the current user."""
            if not change or not obj.created_by:
                obj.created_by = request.user
            obj.updated_by = request.user
            super().save_model(request, obj, form, change)