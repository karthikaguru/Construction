from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, ProjectForm,StageForm
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

def project_list(request, client_id=None):
    if client_id:
        projects = Project.objects.filter(client_id=client_id)
    else:
        projects = Project.objects.all()
    return render(request, 'projectsite/project_list.html', {'projects': projects})


@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projectsite/project_detail.html', {'project': project})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Project
from .forms import ProjectForm

@login_required
def project_add_view(request):
    clients = Client.objects.filter(user=request.user)
    
    if request.method == 'POST' and 'selected_client' in request.POST:
        selected_client_id = request.POST.get('selected_client')
        client = get_object_or_404(Client, id=selected_client_id, user=request.user)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = client  # Assign the selected client to the project
            project.save()
            return redirect('project_list')
    else:
        if clients.exists() and clients.count() == 1:
            client = clients.first()
            form = ProjectForm()
            return render(request, 'projectsite/project_add.html', {'form': form, 'client': client})
        elif clients.exists() and clients.count() > 1:
            return render(request, 'projectsite/select_client.html', {'clients': clients})
        else:
            return redirect('client_create')

    return render(request, 'projectsite/project_add.html', {'form': form, 'client': client})




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
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('/site/success/')  # Change to your success URL
    return render(request, 'projectsite/project_delete.html', {'project': project})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Client, Project, Expense
import json

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

