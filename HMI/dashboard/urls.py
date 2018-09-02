from . import views
from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView
import os
from django.urls import reverse_lazy

app_name = 'dashboard'

urlpatterns = [
    re_path(r'^signup/?$', views.SignUpView.as_view(), name='signup'),
    re_path(r'^about/?$', views.AboutPage.as_view(), name="about"),
    re_path(r'^dashboard/?$', views.DashboardView.as_view(), name="dashboard"),
    re_path(r'^login/?$', LoginView.as_view(
        template_name=os.path.join("dashboard", "login.html")), name="login"),
    re_path(r'^logout/?$', LogoutView.as_view(
        template_name=os.path.join("dashboard", "logout.html")
    ), name="logout"),
]