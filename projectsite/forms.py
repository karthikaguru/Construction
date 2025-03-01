from django import forms
from django.contrib.auth.models import User
from .models import Client, Project, Expense, Milestone,Upload,Stage

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ClientOnboardingForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name','last_name', 'phone_number', 'email', 'site_location', 'site_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
            'site_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Location', 'autocomplete': 'off'}),
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Name', 'autocomplete': 'off'}),
        }

class ProjectOnboardingForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'start_date', 'end_date', 'project_budget', 'documents']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'project_budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Project Budget'}),
            'documents': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = '__all__'



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = '__all__'


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
