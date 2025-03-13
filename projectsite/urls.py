from django.urls import path
from django.views.generic import TemplateView
from projectsite import views

urlpatterns = [
    path('client/create/', views.client_create_view, name='client_create'),
    path('client/<int:client_id>/', views.client_details, name='client_details'),
    path('client/edit/<int:client_id>/', views.client_edit_view, name='client_edit'),
    path('client/delete/<int:client_id>/',views.client_delete_view, name='client_delete'),
    path('clients/', views.client_list, name='client_list'),
    path('client/dashboard/', views.client_dashboard_view, name='client_dashboard_view'),
    path('status-update/<int:project_id>/',views.status_update_view, name='status_update'),
    path('success/', TemplateView.as_view(template_name='projectsite/success.html'), name='success'),
    # url for project
    path('project/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/add/', views.project_add_view, name='project_add'),
    path('projects/client/<int:client_id>/', views.project_list_by_client, name='project_list_by_client'),
    path('project/<int:project_id>/edit/', views.project_edit_view, name='project_edit'),
    path('project/<int:project_id>/delete/', views.project_delete_view, name='project_delete'),
    path('dashboard/',views. project_dashboard_view, name='project_dashboard_view'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/stages/', views.stage_list, name='stage_list'),
    # url for stages
    path('stage/<int:id>/', views.stage_details, name='stage_details'),
    path('project/<int:project_id>/stages/add/', views.stage_add, name='stage_add'),
    path('stage/<int:stage_id>/edit/', views.stage_edit, name='stage_edit'),
    path('stage/<int:stage_id>/delete/', views.stage_delete, name='stage_delete'),
    path('stage_list/<int:project_id>/', views.stage_list, name='stage_list'),
    #url for expense
    path('projects/<int:project_id>/expenses/', views.expense_list, name='expense_list'),
    path('projects/<int:project_id>/expenses/new/', views.expense_new, name='expense_new'),
    path('projects/<int:project_id>/expenses/<int:expense_id>/', views.expense_details, name='expense_details'),
    path('projects/<int:project_id>/expenses/<int:expense_id>/edit/', views.expense_edit, name='expense_edit'),
    path('projects/<int:project_id>/expenses/<int:expense_id>/delete/', views.expense_delete, name='expense_delete'),
]



