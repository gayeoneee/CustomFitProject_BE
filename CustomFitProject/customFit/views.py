from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

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
