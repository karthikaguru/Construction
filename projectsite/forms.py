from django import forms
from .models import Client, Project, Stage, Expense


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'user', 'name', 'phone_number', 'email', 'site_location',
            'site_name', 'project_start_date', 'project_end_date', 'documents'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'site_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site location'}),
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site name'}),
            'project_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'documents': forms.FileInput(attrs={'class': 'form-control'}),
        }



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget', 'description', 'client']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'client': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['project','name', 'due_date', 'completed', 'progress', 'start_date', 'end_date', 'stage_type']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'}),
            'completed': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'}),
            'stage_type': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['project', 'stage', 'description', 'amount_spent', 'date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'stage': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'amount_spent': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'}),
        }
