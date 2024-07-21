from django.contrib import admin
from .models import FoodCategory, Product

admin.site.register(FoodCategory)
admin.site.register(Product)