from rest_framework import serializers
from .models import FoodCategory, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FoodsCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)     #category:product = 1:n

    class Meta:
        model = FoodCategory
        fields = '__all__'