from django.urls import path
from .views import precio_final

urlpatterns = [
    path('products/<int:pk>/precio-final/', precio_final, name='precio_final'),
]
