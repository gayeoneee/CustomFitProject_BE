from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, ProductSearchViewSet, CartViewSet

product_router = SimpleRouter(trailing_slash=False)
product_router.register('product', ProductViewSet, basename='product')

cart_router = SimpleRouter(trailing_slash=False)
cart_router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(product_router.urls)),
    path('search/', ProductSearchViewSet.as_view({'get': 'search'}), name='search'),
    path('search/<int:pk>/', ProductSearchViewSet.as_view({'get': 'retrieve'}), name='search-detail'),
    path('cart/', include(cart_router.urls)),
]
