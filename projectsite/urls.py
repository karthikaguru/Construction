from django.urls import path
from .views import client_onboarding_view, project_dashboard_view, status_update_view

urlpatterns = [
    path('client-onboarding/', client_onboarding_view, name='client_onboarding'),
    path('dashboard/', project_dashboard_view, name='project_dashboard'),
    path('status-update/<int:project_id>/', status_update_view, name='status_update'),
]
