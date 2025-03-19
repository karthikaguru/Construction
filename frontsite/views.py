from django.shortcuts import render,redirect 
from django.contrib.auth.models import User 
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        # Fetch form data
        name = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')  # Expect values: 'admin', 'team_user', 'client'

        # Check if passwords match
        if password1 != password2:
            messages.warning(request, 'The passwords you entered did not match. Please try again.')
            return redirect('register')

        # Check if username already exists
        if CustomUser.objects.filter(username=name).exists():
            messages.warning(request, 'Username already taken. Please choose another one.')
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already registered. Please use a different email.')
            return redirect('register')

        # Create the user if validations pass
        user = CustomUser.objects.create_user(
            username=name,
            email=email,
            password=password1,
        )
       

        # Assign the appropriate role
        if role == 'admin':
            user.role = CustomUser.ADMIN
        elif role == 'team_user':
            user.role = CustomUser.TEAM_USER
        elif role == 'client':
            user.role = CustomUser.CLIENT
        else:
            messages.warning(request, 'Invalid role selected. Please try again.')
            return redirect('register')  # Redirect back if role is invalid

        # Save the user with assigned role
        user.is_staff =True
        user.is_superuser=True
        user.save()

        # Log the user in after successful registration
        login(request, user)
        messages.success(request, 'You have successfully registered. Welcome, {}!'.format(user.username))
        return redirect('/')  # Redirect to a common dashboard or homepage

    # For GET requests, render the registration form
    return render(request, 'frontsite/register.html')


def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')  # Fetch username from the form
        password = request.POST.get('password')  # Fetch password from the form

        # Authenticate the user using username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'Login successful!')

            # Redirect based on the user's role
            if user.role == CustomUser.ADMIN:
                return redirect('site/manage-projects/')
            elif user.role == CustomUser.TEAM_USER:
                return redirect('site/team/dashboard/')
            elif user.role == CustomUser.CLIENT:
                return redirect('site/client/dashboard/')
            else:
                messages.warning(request, 'Invalid user role. Please contact support.')
                return redirect('index')  # Redirect in case of an error
        else:
            # Handle invalid credentials
            messages.warning(request, 'Invalid credentials. Please try again.')
            return redirect('/')

    # Render the login form for GET requests
    return render(request, 'frontsite/login.html')


@login_required
def profile(request):
    messages.success(request, 'Welcome to your profile!')
    messages.success(request,'you are successfully logged in ....')
    return render(request, 'frontsite/profile.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')

def index(request):
     return render(request, 'projectsite/index.html')

