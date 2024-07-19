from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.only('product_id', 'product_name', 'manufacturer', 'category')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ProductSearchViewSet(viewsets.ViewSet):
    def search(self, request):
        product_name = request.query_params.get('product_name', None)
        if product_name:
            queryset = Product.objects.filter(product_name__icontains=product_name).only('product_id', 'product_name', 'manufacturer', 'category')
            if queryset.exists():
                serializer = ProductSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "해당 상품이 없습니다."})
        return Response({"error": "상품명을 입력해 주세요"}, status=400)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "해당 상품이 없습니다"}, status=404)


class CartViewSet(viewsets.ViewSet):
    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    @action(detail=False, methods=['get'])
    def view_cart(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "상품을 선택해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        if cart.cartitem_set.count() >= 5:
            return Response({"error": "상품은 최대 5개까지만 넣을 수 있습니다"}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            return Response({"error": "상품이 이미 맞춤 건강 카드에 담겨있습니다"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "상품을 선택해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=product_id)
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "상품이 맞춤 건강 카드에서 삭제되었습니다"})
        except CartItem.DoesNotExist:
            return Response({"error": "상품이 카드 안에 없습니다"}, status=status.HTTP_400_BAD_REQUEST)