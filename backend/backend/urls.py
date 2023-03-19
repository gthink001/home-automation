from django.contrib import admin
from django.urls import path, include
from core import apis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    path('lambda/get_appliances', apis.get_appliances, name='get_appliances'),
    
    path('lambda/get_switch_state/{endpoint_id}', apis.get_switch_state, name='get_switch_state'),
    path('lambda/set_switch_state/{endpoint_id}/{state}', apis.set_switch_state, name='set_switch_state'),
    
    path('lambda/get_fan_speed/{endpoint_id}', apis.get_fan_speed, name='get_fan_speed'),
    path('lambda/set_fan_speed/{endpoint_id}/{speed}', apis.set_fan_speed, name='set_fan_speed'),
]
