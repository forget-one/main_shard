from django.urls import path
from .views import *
from django.conf import settings
    

urlpatterns = [
    path('category_<slug>/', category, name='category'),
    path('', home, name='home'),
    path('product/<slug>/', product, name='product'),
    path('checkout/', checkout, name='checkout'),
    path('summary/', summary, name='summary'),
    path('add_cart/<slug>/', add_cart, name='add_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('cart_item_single_plus/<slug>/', cart_item_single_plus, name='cart_item_single_plus'),
    path('cart_item_single_minus/<slug>/', cart_item_single_minus, name='cart_item_single_minus'),
]
if settings.DEBUG == True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
