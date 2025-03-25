from django.contrib import admin
from django.urls import path
from frontsite import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('',views.login_view,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout',views.logout_view,name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('index/',views.index,name= 'index'),
    path('contactus/',views.contact_us,name='contactus'),
     path('about/', views.about_us, name='about'), 
]

   
