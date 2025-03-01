from django.shortcuts import render, redirect
from .forms import ClientOnboardingForm, ProjectOnboardingForm,MilestoneForm,ExpenseForm,UploadForm
from .models import Client, Project, Stage, Expense,Milestone,Upload
from django.contrib.auth.decorators import login_required

def  home(request):
    return render(request,'projectsite/home.html')

#  views to handle the form submissions and save the client 
def client_onboarding_view(request):
    if request.method == 'POST':
        client_form = ClientOnboardingForm(request.POST)
        project_form = ProjectOnboardingForm(request.POST, request.FILES)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('/projectsite/project_onboarding_view/')
    else:
        client_form = ClientOnboardingForm()
      
    return render(request, 'projectsite/client_onboarding.html', {'client_form': client_form, 'project_form': project_form})

#  views to handle the form submissions and save the project
def project_onboarding_view(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = ProjectOnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            project_form = form.save(commit=False)
            project_form.client = client
            project_form.save()
            return redirect('/projectsite/')  # Replace with your desired 
    else:
        form = ProjectOnboardingForm()
    return render(request, '/projectsite/project_onboarding.html', {'form': form})

# View to retrieve and display all clients
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


# View to retrieve and display all projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projectsite/project_list.html', {'projects': projects})


@login_required

def dashboard_view(request):
    project = Project.objects.get(client=request.user) # user-->logged in user
    stages = Stage.objects.filter(project=project)
    expenses = Expense.objects.filter(project=project)

    total_spent = sum(expense.amount_spent for expense in expenses)
    budget = project.budget
    balance = budget - total_spent

    context = {
        'project': project,
        'stages': stages,
        'total_spent': total_spent,
        'balance': balance
    }
    return render(request, 'dashboard/dashboard.html', context)


def milestone_list_view(request, project_id):
    milestones = Milestone.objects.filter(project_id=project_id)
    return render(request, 'milestone_list.html', {'milestones': milestones})



def upload_list_view(request, project_id):
    uploads = Upload.objects.filter(project_id=project_id)
    return render(request, 'upload_list.html', {'uploads': uploads})
