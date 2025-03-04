from django.contrib import admin
from .models import Client, Project, Stage, Expense

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'site_location', 'site_name', 'project_start_date', 'project_end_date', 'project_duration', 'project_budget')
    search_fields = ('name', 'email', 'site_name')
    list_filter = ('project_start_date', 'project_end_date')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'budget', 'description')
    search_fields = ('name', 'client__name')
    list_filter = ('client',)

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date')
    search_fields = ('name', 'project__name')
    list_filter = ('project', 'start_date', 'end_date')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'amount_spent', 'date')
    search_fields = ('description', 'project__name')
    list_filter = ('project', 'date')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Expense, ExpenseAdmin)

