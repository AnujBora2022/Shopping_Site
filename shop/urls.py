from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('', views.home, name='home'),
    path('shop', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/order/', views.place_order, name='place_order'),
    path('order/success/', views.order_success, name='order_success'),
    path('add-product/', views.add_product, name='add_product'),  # URL for adding a product
    path('orders/', views.order_list, name='order_list'),  # URL for listing all orders
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),  # New URL for add to cart
    path('cart/', views.view_cart, name='view_cart'),  # New URL for viewing cart
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('all_orders/', views.all_orders, name='all_orders'),
]

# add at the last
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


