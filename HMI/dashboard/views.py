from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import os


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = os.path.join("dashboard", "signup.html")
    success_url = reverse_lazy("dashboard:dashboard")

    def post(self, *args, **kwargs):
        resp = super(SignUpView, self).post(*args, **kwargs)
        return resp


class DashboardView(TemplateView):
    template_name= os.path.join("dashboard", "dashboard.html")
    
class AboutPage(TemplateView):
    template_name=os.path.join("dashboard", "about.html")