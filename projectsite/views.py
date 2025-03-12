from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, ProjectForm,StageForm,ExpenseForm
from .models import Client, Project, Stage, Expense
from django.contrib.auth.decorators import login_required
import json



@login_required
def client_create_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
                client = form.save(commit=False)
                client.user = request.user  # Assign the current logged-in user to the user field
                client.save()

        return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'projectsite/client_create.html', {'form': form})


@login_required
def client_details(request, client_id):
    client = Client.objects.get(id=client_id, user=request.user)
    return render(request, 'projectsite/client_details.html', {'client': client})




@login_required
def client_edit_view(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
        
    return render(request, 'projectsite/client_edit.html', {'form': form, 'client': client})




@login_required
def client_delete_view(request, client_id):
    client =Client.objects.get(id=client_id, user=request.user)
    
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
        
    return render(request, 'projectsite/client_delete.html', {'client': client})



@login_required
def client_dashboard_view(request):
    clients = Client.objects.filter(user=request.user)  # Retrieve all clients associated with the logged-in user
    if not clients.exists():
        return render(request, 'projectsite/no_client.html')
    
    projects = Project.objects.filter(client__in=clients)
    stages = Stage.objects.filter(project__in=projects)
    expenses = Expense.objects.filter(project__in=projects)

    project_names = [project.name for project in projects]
    budgets = [float(project.budget) for project in projects]
    total_spents = [float(sum(expense.amount_spent for expense in Expense.objects.filter(project=project))) for project in projects]

    context = {
        'clients': clients,
        'projects': projects,
        'project_names': json.dumps(project_names),
        'budgets': json.dumps(budgets),
        'total_spents': json.dumps(total_spents),
        'stages': stages,
        'expenses': expenses,
    }
    return render(request, 'projectsite/clientdashboard.html', context)

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'projectsite/client_list.html', {'clients': clients})


# List all projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projectsite/project_list.html', {'projects': projects})

# View details of a single project
def project_details(request, project_id):
    project = Project.objects.get( pk=project_id)
    return render(request, 'projectsite/project_details.html', {'project': project})

# Create a new project
def project_add_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projectsite/project_add.html', {'form': form})

# Edit an existing project
def project_edit(request, pk):
    project = Project.objects.get( pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projectsite/project_form.html', {'form': form})



@login_required
def project_list_view(request):
    projects = Project.objects.filter(client__user=request.user)
    return render(request, 'projectsite/project_list.html', {'projects': projects})


@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/site/success/')  # Change to your success URL
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projectsite/project_edit.html', {'form': form})


@login_required
def project_delete_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  # Change to your success URL
    return render(request, 'projectsite/project_delete.html', {'project': project})


def project_list_by_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    projects = Project.objects.filter(client=client)
    return render(request, 'projectsite/project_list_by_client.html', {'client': client, 'projects': projects})

@login_required
def project_dashboard_view(request):
    clients = Client.objects.filter(user=request.user)  # Retrieve all clients associated with the logged-in user
    if not clients.exists():
        # Redirect to a page where user can create a Client profile or display a friendly message
        return render(request, 'projectsite/no_client.html')
    
    projects = Project.objects.filter(client__in=clients)
    project_names = [project.name for project in projects]
    budgets = [float(project.budget) for project in projects]
    total_spents = [float(sum(expense.amount_spent for expense in Expense.objects.filter(project=project))) for project in projects]

    context = {
        'clients': clients,
        'projects': projects,
        'project_names': json.dumps(project_names),
        'budgets': json.dumps(budgets),
        'total_spents': json.dumps(total_spents),
    }
    return render(request, 'projectsite/projectdashboard.html', context)


def stage_list(request, project_id):
    project = Project.objects.get( id=project_id)
    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage_list.html', {'project': project, 'stages': stages})



def stage_details(request, id):
    project = get_object_or_404(Project, id=id)
    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage_details.html', {'project': project, 'stages': stages})

def stage_add(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.project = project
            stage.save()
            return redirect('stage_list', project_id=project_id)
    else:
        form = StageForm()
    return render(request, 'projectsite/stage_add.html', {'form': form, 'project': project})

def stage_edit(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('stage_detail', stage_id=stage_id)
    else:
        form = StageForm(instance=stage)
    return render(request, 'projectsite/stage_edit.html', {'form': form})

def stage_delete(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    if request.method == 'POST':
        stage.delete()
        return redirect('stage_list', project_id=stage.project.id)
    return render(request, 'projectsite/stage_confirm_delete.html', {'stage': stage})


# Expense view
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'app/expense_form.html', {'form': form})




def expense_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    expenses = Expense.objects.filter(project=project)
    context = {
        'project': project,
        'expenses': expenses,
    }
    return render(request, 'projectsite/expense_list.html', context)

def expense_details(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    context = {
        'project': project,
        'expense': expense,
    }
    return render(request, 'projectsite/expense_details.html', context)


@login_required
def status_update_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stages = Stage.objects.filter(project=project)
    expenses = Expense.objects.filter(project=project)

    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            if not stage.start_date:
                stage.start_date = form.cleaned_data.get('start_date')  # Ensure start_date is set
            stage.save()
            return redirect('/site/success/') 
    else:
        form = StageForm()

    total_spent = sum(expense.amount_spent for expense in expenses)
    budget = project.budget
    balance = budget - total_spent
    stage_names = [stage.name for stage in stages]
    stage_progress = [stage.progress for stage in stages]

    context = {
        'project': project,
        'stages': stages,
        'form': form,
        'total_spent': total_spent,
        'balance': balance,
        'stage_names': stage_names,
        'stage_progress': stage_progress,
    }
    return render(request, 'projectsite/status_update.html', context)

