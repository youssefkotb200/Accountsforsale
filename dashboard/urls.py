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
    path('add_account', views.add_account, name="add_account"),
    path('delete_account/<int:acc_id>', views.delete_account, name="delete_account"),
    path('trade_requests_all', views.trade_requests_all, name="trade_requests_all"),
    path('accept_trade/<int:trade_id>', views.accept_trade, name="accept_trade"),
    path('decline_trade/<int:trade_id>', views.decline_trade, name="decline_trade"),
]