from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_to_cart/<int:account_id>', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:account_id>', views.remove_from_cart, name="remove_from_cart"),
    path('checkout', views.checkout, name="checkout"),
    path('payment', views.payment, name="payment"),
    path('order_completed/<str:order_number>', views.order_completed, name="order_completed"),
]
