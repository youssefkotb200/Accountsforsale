from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<str:option>', views.accounts, name="accounts"),
    path('search/', views.search, name="search"),
    path('category/<str:slug_name>', views.account_categories, name="account_categories"),
    path('account/<int:acc_id>', views.account, name="account"),
    path('trade_request/<str:account_id>', views.trade_request, name="trade_request")
]
