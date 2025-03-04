from django.shortcuts import render, get_object_or_404
from .models import Client, Project, Stage, Expense
from .forms import ClientForm, ProjectForm, StageForm, ExpenseForm

def client_onboarding_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ClientForm()
    return render(request, 'projectsite/client_onboarding.html', {'form': form})

def project_dashboard_view(request):
    client = Client.objects.get(user=request.user)
    projects = Project.objects.filter(client=client)
    context = {
        'client': client,
        'projects': projects
    }
    return render(request, 'projectsite/project_dashboard.html', context)

def status_update_view(request, project_id):
    project = Project.objects.get( id=project_id)
    stages = Stage.objects.filter(project=project)
    expenses = Expense.objects.filter(project=project)

    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Additional logic to update graphs and reports
    else:
        form = StageForm()

    total_spent = sum(expense.amount_spent for expense in expenses)
    budget = project.budget
    balance = budget - total_spent

    context = {
        'project': project,
        'stages': stages,
        'form': form,
        'total_spent': total_spent,
        'balance': balance
    }
    return render(request, 'projectsite/status_update.html', context)
