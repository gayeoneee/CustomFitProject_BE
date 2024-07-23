from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, CartItem
from .serializers import ProductSerializer, CartItemSerializer

# Product 읽기 전용 API view
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 전체 Product list 반환
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.only('product_id', 'product_name', 'manufacturer', 'Capacity', 'category')
        return super().list(request, *args, **kwargs)
    
    # 특정 product 객체를 반환
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

# Product search
class ProductSearchViewSet(viewsets.ViewSet):
    
    # 쿼리 파라미터 받아, 해당 이름 포함하는 product 객체 반환
    def search(self, request):
        product_name = request.query_params.get('product_name', None)

        if product_name:
            queryset = Product.objects.filter(product_name__icontains=product_name).only('product_id', 'product_name', 'manufacturer', 'Capacity', 'category')
            if queryset.exists():
                serializer = ProductSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "해당 상품이 없습니다."})
        return Response({"error": "상품명을 입력해 주세요"}, status=400) #400 code = 클라이언트측 에러 응답

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "해당 상품이 없습니다"}, status=404)


# 상품을 카트에 추가하는 기능을 제공하는 API 뷰
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):    # 제품을 장바구니에 추가
        user = request.user
        product = get_object_or_404(Product, product_id=product_id)
        cart = user.cart

        if cart.items.count() >= 5:
            return Response({"error": "장바구니에 담을 수 있는 최대 상품 수는 5개입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({"error": "이 상품은 이미 장바구니에 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        CartItem.objects.create(cart=cart, product=product)
        return Response({"success": "상품이 장바구니에 추가되었습니다."}, status=status.HTTP_201_CREATED)

# 장바구니 목록을 조회하는 API 뷰
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):     # 장바구니에 담긴 제품 목록을 반환 
        user = request.user
        cart = user.cart
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)