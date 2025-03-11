from django.contrib import admin
from .models import Client, Project, Stage, Expense

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'site_location', 'site_name', 'project_start_date', 'project_end_date', 'project_duration')
    search_fields = ('name', 'phone_number', 'email', 'site_location', 'site_name')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'budget', 'description')
    search_fields = ('name', 'client__name')
    list_filter = ('client',)

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date', 'completed', 'progress', 'start_date', 'end_date', 'stage_type')
    search_fields = ('name', 'project__name')
    list_filter = ('project', 'stage_type')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'amount_spent', 'date')
    search_fields = ('description', 'project__name')
    list_filter = ('project', 'date')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Expense, ExpenseAdmin)
