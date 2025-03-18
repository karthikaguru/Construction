from django.shortcuts import render,redirect 
from django.contrib.auth.models import User 
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
           messages.warning(request, 'The passwords you entered did not match. Please try again.')
           return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=name).exists():
            messages.warning(request, 'Username already taken. Please choose another one.')
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already registered. Please use a different email.')
            return redirect('register')

        # Create the user if validations pass
        user = User.objects.create_user(username=name, email=email, password=password1)
        user.save()
        messages.success(request, 'You have successfully registered. Please log in.')
        return redirect('login')

    else:
        form = UserRegistrationForm()
        return render(request, 'frontsite/register.html', {'form': form})




@login_required
def profile(request):
    messages.success(request, 'Welcome to your profile!')
    messages.success(request,'you are successfully logged in ....')
    return render(request, 'frontsite/profile.html')



