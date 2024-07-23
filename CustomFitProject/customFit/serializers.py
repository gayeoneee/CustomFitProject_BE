from rest_framework import serializers
from .models import FoodCategory, Product, CartItem

# 제품 정보를 직렬화
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# 카테고리와 관련된 제품 정보를 직렬화
class FoodsCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)     #category:product = 1:n

    class Meta:
        model = FoodCategory
        fields = '__all__'

# 카트 항목을 직렬화
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product']