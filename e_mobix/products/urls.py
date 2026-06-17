from django.urls import path
from . import views
from products.views import debug_products

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path("debug-products/", debug_products, name='debug_products'),
]