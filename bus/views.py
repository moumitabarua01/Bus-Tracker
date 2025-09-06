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
            # Simple validation: username must be at least 3 characters
            username = form.cleaned_data.get('username')
            if len(username) < 3:
                form.add_error('username', 'Username must be at least 3 characters long.')
            else:
                user = form.save()
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'bus/registration/signup.html', {"form": form})

def schedule(request):
    return render(request,'bus/registration/schedule.html')
