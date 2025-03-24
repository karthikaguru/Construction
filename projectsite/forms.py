from django import forms
from .models import Client, Project, Stage, Expense
from decimal import Decimal

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'user', 'name', 'phone_number', 'email', 'site_location',
            'site_name', 'project_start_date', 'project_end_date', 'documents'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name', 'autocomplete': 'off'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'autocomplete': 'off'}),
            'site_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site location', 'autocomplete': 'off'}),
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site name', 'autocomplete': 'off'}),
            'project_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'}),
            'documents': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'name', 'budget', 'length', 'breadth', 'description', 'status']  
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter budget'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter length in feet'}),  
            'breadth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter breadth in feet'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
 


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['project', 'name', 'due_date', 'progress', 'status', 'start_date', 'end_date', 'stage_type']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stage name'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter progress percentage'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'stage_type': forms.Select(attrs={'class': 'form-control'}),
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
