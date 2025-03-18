from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, ProjectForm,StageForm,ExpenseForm
from .models import Client, Project, Stage, Expense, User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Sum
from django.core.exceptions import PermissionDenied

from datetime import date
import json

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_team_user(user):
    return hasattr(user, 'profile') and user.profile.role == 'Team User'

def is_client(user):
    return hasattr(user, 'profile') and user.profile.role == 'Client'


@login_required
def manage_projects(request):
    # Logic for Admin to manage the project lifecycle
    projects = Project.objects.all()
    
    # Optionally, add filters based on status or client
    status_filter = request.GET.get('status')  # Get status filter from URL query parameters
    client_filter = request.GET.get('client')  # Get client filter from URL query parameters

    if status_filter:
        projects = projects.filter(status=status_filter)
    if client_filter:
        projects = projects.filter(client__id=client_filter)
    
    # Handle additional actions like deletion
    if request.method == 'POST':
        project_id = request.POST.get('delete_project')  # Assume a button to delete projects
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            project.delete()
            return redirect('manage_projects')  # Redirect to same view after deletion
    
    # Pass data to the template
    context = {
        'projects': projects,
        'status_options': Project.STATUS_CHOICES,  # Assuming you have status choices defined
        'clients': Client.objects.all(),  # For client filtering if necessary
    }
    return render(request, 'projectsite/admin/manage_projects.html', context)

@login_required
def team_dashboard_view(request):
    # Fetch all projects associated with the Team User's clients
    projects = Project.objects.filter(client__user=request.user)

    # Calculate aggregated data for the dashboard (optional)
    ongoing_projects = projects.filter(status='ongoing').count()
    completed_projects = projects.filter(status='completed').count()
    total_expenses = Expense.objects.filter(project__in=projects).aggregate(total_spent=Sum('amount'))['total_spent'] or 0

    # Prepare context for charts or additional statistics
    project_names = [project.name for project in projects]
    budgets = [float(project.budget) for project in projects]
    total_spents = [float(sum(expense.amount for expense in Expense.objects.filter(project=project))) for project in projects]

    # Pass data to the template
    context = {
        'projects': projects,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'total_expenses': total_expenses,
        'project_names': json.dumps(project_names),
        'budgets': json.dumps(budgets),
        'total_spents': json.dumps(total_spents),
    }
    return render(request, 'projectsite/team/team_dashboard.html', context)

@login_required

def view_project_details(request, project_id):
    # Get the project, ensuring it's linked to the logged-in user's client account
    project = get_object_or_404(Project, id=project_id, client__user=request.user)

    # Fetch related stages and expenses for the project
    stages = Stage.objects.filter(project=project)
    expenses = Expense.objects.filter(project=project)

    # Aggregate financial details
    total_budget = project.budget
    total_spent = expenses.aggregate(total_spent=Sum('amount'))['total_spent'] or 0
    remaining_budget = total_budget - total_spent

    # Prepare context data for the template
    context = {
        'project': project,
        'stages': stages,
        'expenses': expenses,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
    }
    return render(request, 'projectsite/client/project_details.html', context)



@user_passes_test(is_admin)
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
    return render(request, 'projectsite/client/client_create.html', {'form': form})


@login_required
@user_passes_test(is_admin)  # Only Admins can view all client details
def client_details(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'projectsite/client/client_details.html', {'client': client})

@login_required
@user_passes_test(is_team_user)
def client_details(request, client_id):
    client = Client.objects.get(id=client_id, user=request.user)
    return render(request, 'projectsite/client/client_details.html', {'client': client})



@login_required
@user_passes_test(is_admin) 
def client_edit_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'projectsite/client/client_edit.html', {'form': form})

@login_required
@user_passes_test(is_team_user)  # Restrict editing to Team Users for their clients
def client_edit_view(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'projectsite/client/client_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin)  # Admin can view all clients
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'projectsite/client/client_list.html', {'clients': clients})



# For Team Users to view only their clients
@login_required
@user_passes_test(is_team_user)
def client_list_view(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'projectsite/client/client_list.html', {'clients': clients})




@login_required
@user_passes_test(is_admin)
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'projectsite/client/client_delete.html', {'client': client})



@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # User Statistics
    user_count = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    # Dynamic filter for users who joined in the current month
    current_month = date.today().month
    new_users = User.objects.filter(date_joined__month=current_month).count()

    # Project Statistics
    total_projects = Project.objects.count()
    ongoing_projects = Project.objects.filter(status='ongoing').count()
    completed_projects = Project.objects.filter(status='completed').count()

    # Client Statistics
    total_clients = Client.objects.count()

    # Financial Statistics
    total_budget = Project.objects.aggregate(total_budget=Sum('budget'))['total_budget'] or 0
    total_expenses = Expense.objects.aggregate(total_spent=Sum('amount_spent'))['total_spent'] or 0

    # Data for Charts
    project_data = Project.objects.annotate(
        total_spent=Sum('expense__amount_spent')
    )  # Annotates each project with total spent
    project_names = [project.name for project in project_data]
    budgets = [float(project.budget) for project in project_data]
    total_spents = [float(project.total_spent or 0) for project in project_data]

    context = {
        'user_count': user_count,
        'active_users': active_users,
        'new_users': new_users,
        'total_projects': total_projects,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'total_clients': total_clients,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'project_names': json.dumps(project_names),
        'budgets': json.dumps(budgets),
        'total_spents': json.dumps(total_spents),
    }
    return render(request, 'projectsite/admindashboard.html', context)



@login_required
@user_passes_test(is_client)
def client_dashboard_view(request):
    clients = Client.objects.filter(user=request.user)  # Retrieve all clients associated with the logged-in user
   
    
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


# List all projects
@login_required
@user_passes_test(is_admin)  
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projectsite/project/project_list.html', {'projects': projects})

def has_project_access(user):
    if not (is_admin(user) or is_team_user(user) or is_client(user)):
        raise PermissionDenied

@login_required
@user_passes_test(has_project_access)
def project_details(request, project_id):
    # Admins can view all projects
    if is_admin(request.user):
        project = get_object_or_404(Project, id=project_id)
    # Team Users can view projects linked to their assigned clients
    elif is_team_user(request.user):
        project = get_object_or_404(Project, id=project_id, client__user=request.user)
    # Clients can only view their own projects
    elif is_client(request.user):
        project = get_object_or_404(Project, id=project_id, client__user=request.user)
    else:
        # Raise permission denied if none of the roles match
        raise PermissionDenied

    # Render project details
    return render(request, 'projectsite/project/project_details.html', {'project': project})

# Create a new project
@login_required
@user_passes_test(is_admin)
def project_add_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projectsite/project/project_add.html', {'form': form})



@login_required
@user_passes_test(is_team_user)    # Allow only Team Users
def project_list_view(request):
    projects = Project.objects.filter(client__user=request.user)
    return render(request, 'projectsite/project_list.html', {'projects': projects})

# Edit an existing project

def can_edit_project(user):
    return is_admin(user) or is_team_user(user) or is_client(user)

@login_required
@user_passes_test(can_edit_project)  # Allow Admins, Team Users, and Clients
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Admins can edit any project
    if is_admin(request.user):
        pass  # Admins have full access

    # Team Users can only edit projects linked to their assigned clients
    elif is_team_user(request.user) and project.client.user != request.user:
        raise PermissionDenied

    # Clients can only edit their own projects
    elif is_client(request.user) and project.client.user != request.user:
        raise PermissionDenied

    # Handle GET and POST requests
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Redirect to the project list
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projectsite/project/project_edit.html', {'form': form})


@login_required
def project_delete_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  
    return render(request, 'projectsite/project/project_delete.html', {'project': project})


def project_list_by_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    projects = Project.objects.filter(client=client)
    return render(request, 'projectsite/project/project_list_by_client.html', {'client': client, 'projects': projects})



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
        'project_names': project_names,  # Pass the list directly
        'budgets': budgets, 
        'total_spents': total_spents,  
    }
    return render(request, 'projectsite/projectdashboard.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def stage_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Restrict Team Users to their assigned projects
    if is_team_user(request.user) and project.client.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.project = project
            stage.save()
            return redirect('stage_list', project_id=project.id)
    else:
        form = StageForm()
    return render(request, 'projectsite/stage/stage_add.html', {'form': form, 'project': project})


@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def stage_edit(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    project = stage.project

    # Restrict Team Users to their assigned projects
    if is_team_user(request.user) and project.client.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('stage_list', project_id=project.id)
    else:
        form = StageForm(instance=stage)

    return render(request, 'projectsite/stage/stage_edit.html', {'form': form, 'project': project})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def stage_delete(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    project_id = stage.project.id

    # Restrict Team Users to their assigned projects
    if is_team_user(request.user) and stage.project.client.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        stage.delete()
        return redirect('project_details', project_id=project_id)
    return render(request, 'projectsite/stage/stage_delete.html', {'stage': stage})


@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u) or is_client(u))  # Allow all roles
def stages_list_by_client(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Restrict Team Users and Clients to their assigned projects
    if (is_team_user(request.user) or is_client(request.user)) and project.client.user != request.user:
        raise PermissionDenied

    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_list_by_client.html', {'project': project, 'stages': stages})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u) or is_client(u))  # Allow all roles
def stage_details(request, project_id, stage_id):
    project = get_object_or_404(Project, id=project_id)
    stage = get_object_or_404(Stage, id=stage_id, project=project)

    # Restrict Team Users and Clients to their assigned projects
    if (is_team_user(request.user) or is_client(request.user)) and project.client.user != request.user:
        raise PermissionDenied

    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_details.html', {'stage': stage, 'project': project, 'stages': stages})


@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u) or is_client(u))  # Allow all roles
def stage_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Restrict Team Users and Clients to their assigned projects
    if (is_team_user(request.user) or is_client(request.user)) and project.client.user != request.user:
        raise PermissionDenied

    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_list.html', {'project': project, 'stages': stages})



def can_access_expense(user, project):
    if is_admin(user):
        return True
    elif is_team_user(user) and project.client.user == user:
        return True  # Team Users can access expenses of their assigned clients
    elif is_client(user) and project.client.user == user:
        return True  # Clients can view their own project expenses
    return False


#Add new expense
@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def expense_new(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_expense(request.user, project):
        raise PermissionDenied

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect('expense_details', project_id=project.id, expense_id=expense.id)
    else:
        form = ExpenseForm()
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'projectsite/expense/expense_edit.html', context)



@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u) or is_client(u))  # Allow all roles
def expense_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_expense(request.user, project):
        raise PermissionDenied

    expenses = Expense.objects.filter(project=project)
    context = {
        'project': project,
        'expenses': expenses,
    }
    return render(request, 'projectsite/expense/expense_list.html', context)

# view expense details
@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u) or is_client(u))  # Allow all roles
def expense_details(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_expense(request.user, project):
        raise PermissionDenied

    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    context = {
        'project': project,
        'expense': expense,
    }
    return render(request, 'projectsite/expense/expense_details.html', context)

#edit expense
@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def expense_edit(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_expense(request.user, project):
        raise PermissionDenied

    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect('expense_details', project_id=project.id, expense_id=expense.id)
    else:
        form = ExpenseForm(instance=expense)
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'projectsite/expense/expense_edit.html', context)

#delete expense
@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  # Allow Admins and Team Users
def expense_delete(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_expense(request.user, project):
        raise PermissionDenied

    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    expense.delete()
    return redirect('expense_list', project_id=project.id)


@login_required
@user_passes_test(lambda u: is_admin(u) or is_team_user(u))  
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

