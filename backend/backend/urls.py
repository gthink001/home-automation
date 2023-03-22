from django.contrib import admin
from django.urls import path, include
from core import apis
from core import google_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    path('lambda/get_appliances', apis.get_appliances, name='get_appliances'),
    
    path('lambda/get_switch_state/<str:endpoint_id>', apis.get_switch_state, name='get_switch_state'),
    path('lambda/set_switch_state/<str:endpoint_id>/<str:state>', apis.set_switch_state, name='set_switch_state'),
    
    path('lambda/get_fan_speed/<str:endpoint_id>', apis.get_fan_speed, name='get_fan_speed'),
    path('lambda/set_fan_speed/<str:endpoint_id>/<int:speed>', apis.set_fan_speed, name='set_fan_speed'),

    path('google_actions/', google_webhook.google_actions, name='google_actions'),

]
