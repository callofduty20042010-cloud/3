from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_new', 'is_discounted')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_new', 'is_discounted')
    search_fields = ('title', 'description')
    list_editable = ('price', 'is_new', 'is_discounted')
    list_per_page = 10



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    ...

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    ...

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price')
    list_filter = ('product', 'quantity')
    search_fields = ('product', 'quantity')
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price')
    list_filter = ('customer', )
    search_fields = ('customer', )
    list_per_page = 10

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'total')
    list_filter = ('product', 'amount', 'total')
    search_fields = ('product', )