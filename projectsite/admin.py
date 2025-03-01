from django.contrib import admin
from .models import Client,Project, Stage, Milestone,Expense
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name','' 'phone_number', 'email', 'site_location', 'site_name', 'user')
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('client', 'start_date', 'end_date', 'project_budget', 'documents', 'project_duration')
    
admin.site.register(Stage)
admin.site.register(Expense)
admin.site.register(Milestone)
    
