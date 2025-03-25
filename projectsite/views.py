from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, ProjectForm,StageForm,ExpenseForm
from .models import Client, Project, Stage, Expense, User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
import json

User = get_user_model()
from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

def manage_projects(request):
    # Fetch all projects and calculate total expenses and total land area dynamically
    projects = Project.objects.annotate(
        total_expenses=Sum('expenses__amount_spent'),  # Sum up related 'amount_spent' fields from Expense model
        total_land_area=ExpressionWrapper(
            F('length') * F('breadth'), output_field=DecimalField(max_digits=10, decimal_places=2)
        )  # Dynamically calculate total area
    )

    # Get the selected status from POST request
    selected_status = request.POST.get('status', '').strip() if request.method == 'POST' else ''
    if selected_status:
        projects = projects.filter(status=selected_status)

    # Calculate financial totals across all filtered projects
    total_budget = projects.aggregate(Sum('budget'))['budget__sum'] or 0
    total_expenses = projects.aggregate(Sum('total_expenses'))['total_expenses__sum'] or 0
    total_profit = total_budget - total_expenses
    total_land_area = projects.aggregate(Sum('total_land_area'))['total_land_area__sum'] or 0

    # Prepare context for the template
    context = {
        'projects': projects,  
        'status_options': Stage.STATUS_CHOICES,  # Available statuses for filtering
        'selected_status': selected_status,  # Selected status to maintain state in the template
        'total_budget': total_budget,  # Total budget of filtered projects
        'total_expenses': total_expenses,  # Total expenses of filtered projects
        'total_profit': total_profit,  # Profit calculation
        'total_land_area': total_land_area,  # Total land area of all projects
    }
    
    return render(request, 'projectsite/admin/manage_projects.html', context)


@login_required
def client_create_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
                form.save()
               

        return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'projectsite/client/client_create.html', {'form': form})


@login_required
def client_details(request, client_id):
    client = Client.objects.get(id=client_id, user=request.user)
    return render(request, 'projectsite/client/client_details.html', {'client': client})




@login_required
def client_edit_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
        
    return render(request, 'projectsite/client/client_edit.html', {'form': form, 'client': client})




@login_required
def client_delete_view(request, client_id):
    client =Client.objects.get(id=client_id, user=request.user)
    
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
        
    return render(request, 'projectsite/client/client_delete.html', {'client': client})




@login_required
def client_dashboard_view(request):
    # Get all clients for the logged-in user
    clients = Client.objects.filter(user=request.user)

    # Get all projects associated with these clients
    projects = Project.objects.filter(client__in=clients).annotate(
        total_spent=Sum('expenses__amount_spent')  # Annotates the total spent for each project
    )

    # Prepare chart data
    project_names = [project.name for project in projects]
    budgets = [float(project.budget) for project in projects]
    total_spents = [project.total_spent or 0 for project in projects]

    # Prepare the context for rendering
    context = {
        'clients': clients,
        'projects': projects,
        'project_names': json.dumps(project_names, cls=DjangoJSONEncoder),
        'budgets': json.dumps(budgets, cls=DjangoJSONEncoder),
        'total_spents': json.dumps(total_spents, cls=DjangoJSONEncoder),
         }
    return render(request, 'projectsite/client/clientdashboard.html', context)



def client_list(request):
    clients = Client.objects.all()
    return render(request, 'projectsite/client/client_list.html', {'clients': clients})

# List all projects
@login_required
def project_list(request, client_id=None):
    if client_id:
        projects = Project.objects.filter(client_id=client_id)
    else:
        projects = Project.objects.all()
    return render(request, 'projectsite/project/project_list.html', {'projects': projects})


@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projectsite/project/project_detail.html', {'project': project})


def project_list_by_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    projects = Project.objects.filter(client=client)
    return render(request, 'projectsite/project/project_list_by_client.html', {'client': client, 'projects': projects})


@login_required
# Create a new project only for admin
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
# Allow Admins, Team Users, and Clients  Admins can edit any project
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_list')  # Redirect to project list
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projectsite/project/project_edit.html', {'form': form, 'project': project})




@login_required
#Allow only Team Users
def project_list_view(request):
    projects = Project.objects.filter(client__user=request.user)
    return render(request, 'projectsite/project_list.html', {'projects': projects})



@login_required
def project_delete_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  
    return render(request, 'projectsite/project/project_delete.html', {'project': project})


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

@login_required
#@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # User Statistics
    user_count = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    # Dynamic filter for users who joined in the current month
    current_month = date.today().month
    new_users = User.objects.filter(date_joined__month=current_month).count()

    # Project Statistics
    total_projects = Project.objects.count()
    ongoing_projects = Project.objects.filter(status='in_progress').count()
    completed_projects = Project.objects.filter(status='completed').count()

    # Client Statistics
    total_clients = Client.objects.count()

    # Financial Statistics
    total_budget = Project.objects.aggregate(total_budget=Sum('budget'))['total_budget'] or 0
    total_expenses = Expense.objects.aggregate(total_spent=Sum('amount_spent'))['total_spent'] or 0

    # Data for Charts
    project_data = Project.objects.annotate(
        total_spent=Sum('expenses__amount_spent')
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
    return render(request, 'projectsite/admin/admindashboard.html', context)



@login_required
 # Allow Admins and Team Users
def stage_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
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
 # Allow Admins and Team Users
def stage_edit(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    project = stage.project

    # Restrict Team Users to their assigned projects
    

    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('stage_list', project_id=project.id)
    else:
        form = StageForm(instance=stage)

    return render(request, 'projectsite/stage/stage_edit.html', {'form': form, 'project': project})

@login_required
  # Allow Admins and Team Users
def stage_delete(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    project_id = stage.project.id

    # Restrict Team Users to their assigned projects
    if request.method == 'POST':
        stage.delete()
        return redirect('project_details', project_id=project_id)
    return render(request, 'projectsite/stage/stage_delete.html', {'stage': stage})


@login_required
  # Allow all roles
def stages_list_by_client(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_list_by_client.html', {'project': project, 'stages': stages})

@login_required
 # Allow all roles
def stage_details(request, project_id, stage_id):
    project = get_object_or_404(Project, id=project_id)
    stage = get_object_or_404(Stage, id=stage_id, project=project)

    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_details.html', {'stage': stage, 'project': project, 'stages': stages})


@login_required
 # Allow all roles
def stage_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Restrict Team Users and Clients to their assigned projects
    stages = Stage.objects.filter(project=project)
    return render(request, 'projectsite/stage/stage_list.html', {'project': project, 'stages': stages})


#Add new expense  Allow Admins and Team Users
@login_required
def expense_new(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
   

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
 # Allow all roles
def expense_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    expenses = Expense.objects.filter(project=project)
    context = {
        'project': project,
        'expenses': expenses,
    }
    return render(request, 'projectsite/expense/expense_list.html', context)

# view expense details
@login_required
# Allow all roles
def expense_details(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    context = {
        'project': project,
        'expense': expense,
    }
    return render(request, 'projectsite/expense/expense_details.html', context)

#edit expense
@login_required
# Allow Admins and Team Users
def expense_edit(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
    
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

#delete expense # Allow Admins and Team Users

@login_required
def expense_delete(request, project_id, expense_id):
    project = get_object_or_404(Project, pk=project_id)
  

    expense = get_object_or_404(Expense, pk=expense_id, project=project)
    expense.delete()
    return redirect('expense_list', project_id=project.id)


@login_required
# admin or team user
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

