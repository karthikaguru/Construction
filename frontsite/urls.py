from django.contrib import admin
from django.urls import path
from frontsite import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('',views.login_view,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout',views.logout_view,name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('index/',views.index,name= 'index'),
    path('contactus/',views.contact_us,name='contactus'),
     path('about/', views.about_us, name='about'), 
]

   
