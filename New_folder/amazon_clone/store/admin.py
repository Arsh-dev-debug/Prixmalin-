from django.contrib import admin
from .models import Product, Review, Cart, Order, OrderItem

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price', 'release_date')
    list_filter = ('manufacturer', 'release_date')
    search_fields = ('name', 'description', 'manufacturer')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'release_date')
    list_filter = ('rating', 'release_date')
    search_fields = ('author', 'body')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_time')
    list_filter = ('order',)
    search_fields = ('order__id', 'product__name')