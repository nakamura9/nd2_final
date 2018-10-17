from . import views
from django.conf.urls import url

app_name = 'api'

urlpatterns = [
    url(r'^get-status/?$', views.get_status ,name='get-status'),
    url(r'^get-color-status/?$', views.get_color_status ,
        name='get-color-status'),
    url(r'^image-upload/?$', views.image_upload, name='image-upload'),
    url(r'^toggle-printer/?$', views.toggle_printer, name='toggle-printer'),
    url(r'^toggle-machine-mode/?$', views.toggle_machine_mode,
        name='toggle-machine-mode'),
    url(r'^toggle-color-mode/?$', views.toggle_color_mode, name='toggle-color-mode'),
    url(r'^set-color-setpoint/?$', views.set_color_setpoint, 
        name='set-color-setpoint'),
    url(r'^toggle-pigment-valve/?$', views.toggle_pigment_valve, 
        name='toggle-pigment-valve'),
    url(r'^toggle-base-valve/?$', views.toggle_base_valve, name='toggle-base-valve'),
    url(r'^toggle-agitator/?$', views.toggle_agitator, name='toggle-agitator'),
    url(r'^get-events/?$', views.get_events, name='get-events'),
    url(r'^get-register-positions/?$', views.get_register_positions, 
        name='get-register-positions'),
]