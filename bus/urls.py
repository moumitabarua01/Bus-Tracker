
from django.urls import path,include
from . import views
# from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="bus/registration/login.html"), name="login"),
    path("signup/", views.authView, name="signup"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("schedule", views.schedule,name='schedule'),
]
