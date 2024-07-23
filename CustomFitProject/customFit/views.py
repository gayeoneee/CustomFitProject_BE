from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import get_user_model
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
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 사용 가능 (로그인)

    def post(self, request, product_id):    # 제품을 카트에 추가
        user = request.user
        product = get_object_or_404(Product, product_id=product_id)
        cart = user.cart

        if cart.items.count() >= 5:
            return Response({"error": "카트에 담을 수 있는 최대 상품 수는 5개입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({"error": "이 상품은 이미 카트에 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        CartItem.objects.create(cart=cart, product=product)
        return Response({"success": "상품이 카트에 추가되었습니다."}, status=status.HTTP_201_CREATED)

# 카트 목록을 조회하는 API 뷰
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):     # 카트에 담긴 제품 목록을 반환 
        user = request.user
        cart = user.cart
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


# 상품을 카트에서 삭제하는 기능을 제공하는 API 뷰
class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):  # 제품을 카트에서 삭제
        user = request.user
        product = get_object_or_404(Product, product_id=product_id)
        cart = user.cart

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"success": "상품이 카트에서 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "카트에 해당 상품이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 카트 안의 모든 상품을 삭제하는 기능을 제공하는 API 뷰      
class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):  # 카트에 있는 모든 제품을 삭제
        user = request.user
        cart = user.cart
        cart.items.all().delete()
        return Response({"success": "카트가 비워졌습니다."}, status=status.HTTP_204_NO_CONTENT)
    

User = get_user_model() # 현재 활성 사용자 모델 반환/ settings.AUTH_USER_MODEL에 지정된 사용자 모델을 반환

# 비교기능
class CompareProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = user.cart.items.all()

        if not user.keyword:
            return Response({"error": "사용자의 키워드가 설정되어 있지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not cart_items:
            return Response({"error": "카트에 상품이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        keyword_id = user.keyword.keyword_id
        if keyword_id == 1:  # 당뇨
            sorted_items = sorted(cart_items, key=lambda x: x.product.sugars)   #오름차순
        elif keyword_id == 2:  # 비만
            sorted_items = sorted(cart_items, key=lambda x: x.product.calories) #오름차순
        elif keyword_id == 3:  # 고혈압
            sorted_items = sorted(cart_items, key=lambda x: x.product.sodium)   #오름차순
        elif keyword_id == 4:  # 근손실
            sorted_items = sorted(cart_items, key=lambda x: x.product.protein, reverse=True)    #내림차순
        else:
            return Response({"error": "알 수 없는 키워드입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        best_product = sorted_items[0].product
        serializer = ProductSerializer(best_product)

        user.cart.items.all().delete()  # 비교 완료 후 카트 비우기

        return Response(serializer.data, status=status.HTTP_200_OK)