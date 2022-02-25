from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login_view"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout_view"),
    path('change_avatar/<str:avatar_url>', views.change_avatar, name="change_avatar"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('resetpassword/<uidb64>/<token>/', views.resetpassword, name='resetpassword'),
    path('resetpassword_form', views.resetpassword_form, name="resetpassword_form")
]
