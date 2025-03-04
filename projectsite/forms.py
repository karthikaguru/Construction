from django import forms
from .models import Client, Project, Stage, Expense

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'email', 'site_location', 'site_name', 'project_start_date', 'project_end_date', 'project_budget', 'documents']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget', 'description']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['project', 'name', 'due_date', 'completed', 'progress', 'stage_type']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount_spent', 'date']
