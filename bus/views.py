from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

@login_required
def home(request):
    return render(request, 'home.html')

def authView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after signup
            login(request, user)
            return redirect('home')  # Redirect to home after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'bus/registration/signup.html', {"form": form})

def schedule(request):
    return render(request,'bus/registration/schedule.html')
