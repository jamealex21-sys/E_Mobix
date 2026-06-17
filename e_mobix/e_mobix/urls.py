from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.http import HttpResponse

from accounts import views as accounts_views
from cart import views as cart_views
from orders import views as orders_views
from products.views import debug_products


def debug_users(request):
    return HttpResponse(
        "<br>".join(
            f"{u.username} | staff={u.is_staff} | super={u.is_superuser}"
            for u in User.objects.all()
        )
    )


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('cart/', cart_views.cart_view, name='cart_view'),
    path(
        'cart/remove/<str:cart_key>/',
        cart_views.remove_from_cart,
        name='remove_from_cart'
    ),

    path('checkout/', orders_views.checkout, name='checkout'),

    path('login/', accounts_views.login_view, name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view, name='logout'),

    path('debug/', debug_products, name='debug_products'),
    path('debug-products/', debug_products),
    path('debug-users/', debug_users),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )