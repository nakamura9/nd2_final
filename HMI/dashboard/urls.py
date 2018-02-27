import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
import os
from django.urls import reverse_lazy


urlpatterns = [
    url(r'^signup/?$', views.SignUpView.as_view(), name='signup'),
    url(r'^about/?$', views.AboutPage.as_view(), name="about"),
    url(r'^dashboard/?$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^login/?$', LoginView.as_view(
        template_name=os.path.join("dashboard", "login.html")), name="login"),
    url(r'^logout/?$', LogoutView.as_view(
        template_name=os.path.join("dashboard", "logout.html")
    ), name="logout"),
]