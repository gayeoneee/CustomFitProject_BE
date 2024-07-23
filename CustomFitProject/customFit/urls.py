from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, ProductSearchViewSet
from .views import AddToCartView, CartDetailView, CartItemDeleteView, CartClearView
from .views import CompareProductsView

product_router = SimpleRouter()
product_router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(product_router.urls)),
    
    # 상품 검색
    path('search/', ProductSearchViewSet.as_view({'get': 'search'}), name='search'),
    path('search/<int:pk>/', ProductSearchViewSet.as_view({'get': 'retrieve'}), name='search-detail'),
    
    # 카트 
    path('add_cart/<int:product_id>/', AddToCartView.as_view(), name='add_cart'),   # 카트에 상품 추가
    path('cart/', CartDetailView.as_view(), name='cart'),    # 카트 안에 상품 보기
    path('cart/delete_item/<int:product_id>/', CartItemDeleteView.as_view(), name='delete_cart_item'),  # 특정 상품 삭제 경로
    path('cart/clear/', CartClearView.as_view(), name='clear_cart'),  # 모든 상품 삭제 경로

    # 상품 비교
    path('compare/', CompareProductsView.as_view(), name='compare_products'),
]
