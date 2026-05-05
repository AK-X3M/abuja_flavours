from django.contrib import admin
from .models import Category, Meal, Cart, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'meal', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'net_total', 'payment_method', 'status', 'created_at']

admin.site.register(OrderItem)
