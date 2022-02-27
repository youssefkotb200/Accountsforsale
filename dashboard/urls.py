from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('my_orders', views.my_orders, name="my_orders"),
    path('order/<int:order_number>', views.order, name="order"),
    path('selling_accounts', views.selling_accounts, name="selling_accounts"),
    path('sold_accounts', views.sold_accounts, name="sold_accounts"),
    path('profile', views.profile, name="profile"),
]
