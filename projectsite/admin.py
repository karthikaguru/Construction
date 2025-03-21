from django.contrib import admin
from .models import Client, Project, Stage, Expense

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'site_location', 'site_name', 'project_start_date', 'project_end_date', 'project_duration')
    search_fields = ('name', 'phone_number', 'email', 'site_location', 'site_name')



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'budget', 'description', 'status')  # Added 'status' for visibility
    search_fields = ('name', 'client__name', 'description')  # Included 'description' for advanced search
    list_filter = ('client', 'status')  # Added filtering by 'status'

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date', 'start_date', 'end_date', 'progress', 'stage_type', 'status')  # Added 'status' for clarity
    search_fields = ('name', 'project__name', 'stage_type')  # Included 'stage_type' for advanced search
    list_filter = ('project', 'stage_type', 'status')  # Added filtering by 'status'


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'amount_spent', 'date')
    search_fields = ('description', 'project__name')
    list_filter = ('project', 'date')


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Expense, ExpenseAdmin)
