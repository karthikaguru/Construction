from django.contrib import admin
from django.urls import path
from frontsite import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('',auth_views.LoginView.as_view(template_name='frontsite/login.html'),name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout',auth_views.LogoutView.as_view(template_name='frontsite/logout.html'),name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

   
