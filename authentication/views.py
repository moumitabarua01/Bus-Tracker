from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomLoginForm, CustomPasswordChangeForm, UserProfileForm
from .models import UserProfile


def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Send welcome email
            send_welcome_email(user)
            
            messages.success(request, 'Account created successfully! Please check your email for confirmation.')
            return redirect('authentication:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def password_change_view(request):
    """Password change view"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('authentication:profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'authentication/password_change.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('authentication:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'authentication/profile.html', {'form': form, 'profile': profile})


def send_welcome_email(user):
    """Send welcome email to newly registered user"""
    subject = 'Welcome to Bus Tracker!'
    
    html_message = render_to_string('authentication/email/welcome_email.html', {
        'user': user,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'
    })
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send welcome email: {e}")


@login_required
def dashboard_view(request):
    """User dashboard view"""
    return render(request, 'authentication/dashboard.html', {
        'user': request.user
    })
