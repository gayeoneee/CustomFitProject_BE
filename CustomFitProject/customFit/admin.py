from django.contrib import admin
from .models import FoodCategory, Product, Cart, CartItem

admin.site.register(FoodCategory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)