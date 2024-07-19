from rest_framework import serializers
from .models import FoodCategory, Product, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FoodsCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)     #category:product = 1:n

    class Meta:
        model = FoodCategory
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']