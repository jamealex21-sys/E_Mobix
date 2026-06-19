from django.urls import path
from . import views

urlpatterns = [
    # វាយលីង: /accounts/login/
    path('login/', views.login_view, name='login'),
    
    # វាយលីង: /accounts/register/
    path('register/', views.register_view, name='register'),
    
    # វាយលីង: /accounts/logout/
    path('logout/', views.logout_view, name='logout'),
    
    # វាយលីង: /accounts/dashboard/
    path('dashboard/', views.user_dashboard, name='dashboard_user'),
    
    # វាយលីង: /accounts/profile/
    path('profile/', views.user_profile, name='user_profile'),
    
    # វាយលីង: /accounts/orders/<order_id>/
    path('orders/<int:order_id>/', views.order_detail, name='user_order_detail'),
]