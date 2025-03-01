from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.home,name='home'),
    path('client_onboarding/',views.client_onboarding_view,name='client_onboarding'),
    path('project_onboarding/',views.project_onboarding_view,name='project_onboarding'),
    path('clients/', views.client_list, name='clients_list'),
    path('projects/', views.project_list, name='projects_list'),
    path('dashboard/', views.dashboard_view, name='task_dashboard'),
    path('uploads/',views. upload_list_view, name='expense_dashboard'),
    path('milestones/',views.milestone_list_view, name='milestone_dashboard'),
]

  