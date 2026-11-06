from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet, precio_final

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/precio-final/', precio_final, name='precio_final'),
]
