from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect 
from django.contrib.auth.models import User 
from .forms import UserRegistrationForm
from django.contrib import messages


def register(request):
      if request.method == 'POST':
                 name =request.POST.get('username')
                 email= request.POST.get('email')
                 password1 =request.POST.get('password1')
                 password2=request.POST.get('password2')
                 if password1 == password2:
                    user=User.objects.create_user(username=name,email=email,password=password1)
                    user.save()
                    messages.success(request,'you are successfully logged in ....')
                    return redirect('login')
                 else:
                    messages.warning(request,'Password Mismatched give corrct password ....')
                    return redirect('register')
                 
      else:
            form =UserRegistrationForm()
            return render(request,'frontsite/register.html',{'form':form})

def profile(request):
          messages.success(request,'you are successfully logged in ....')
          return render(request,'frontsite/profile.html')

