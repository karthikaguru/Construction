from django.urls import path
from django.views.generic import TemplateView
from .views import client_create_view,client_details,client_list, client_edit_view, client_delete_view, project_dashboard_view,status_update_view,project_details, project_edit_view, project_delete_view,project_list,client_dashboard_view,project_add_view


urlpatterns = [
    path('client/create/', client_create_view, name='client_create'),
    path('client/<int:client_id>/', client_details, name='client_details'),
    path('client/edit/<int:client_id>/', client_edit_view, name='client_edit'),
    path('client/delete/<int:client_id>/', client_delete_view, name='client_delete'),
    path('clients/', client_list, name='client_list'),
    path('client/dashboard/', client_dashboard_view, name='client_dashboard_view'),
    path('status-update/<int:project_id>/', status_update_view, name='status_update'),
    path('success/', TemplateView.as_view(template_name='projectsite/success.html'), name='success'),
    path('project/<int:project_id>/', project_details, name='project_details'),
    path('projects/add/', project_add_view, name='project_add'),
    path('project/<int:project_id>/edit/', project_edit_view, name='project_edit'),
    path('project/<int:project_id>/delete/', project_delete_view, name='project_delete'),
    path('dashboard/', project_dashboard_view, name='project_dashboard_view'),
    path('projects/', project_list, name='project_list'),
    path('projects/<int:client_id>/', project_list, name='project_list_by_client'),
]



