from django.http import JsonResponse
from oauth2_provider.decorators import protected_resource
import requests

@protected_resource()
def get_appliances(request):
    print(request.user, "request.user")
    appliances = [
        {
            "applianceId": "C44F330C30A5T1",
            "manufacturerName": "G-Think",
            "modelName": "Switch",
            "version": "1",
            "friendlyName": "Switch",
            "friendlyDescription": "001 Switch that can only be turned on/off",
            "isReachable": True,
            "actions": [
                "turnOn",
                "turnOff"
            ],
            "additionalApplianceDetails": {
            }
        },
        {
            "applianceId": "840D8ED6A060F1",
            "manufacturerName": "G-Think",
            "modelName": "Fan",
            "version": "1",
            "friendlyName": "Fan",
            "friendlyDescription": "002 fan",
            "isReachable": True,
            "actions": [
                "setPercentage"
            ],
            "additionalApplianceDetails": {}
        },
    ]
    return JsonResponse(appliances, safe=False)


@protected_resource()
def get_switch_state(request, endpoint_id):    
    url = f'https://www.gthinkinventors.in/api/gthink/alexa_state/{endpoint_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        state_data = response.json()
        state = "ON" if state_data["State"] == "1" else "OFF"
        print(url, "url")
        print(state, "state")
        return JsonResponse({"state": state})
    else:
        return JsonResponse({"error": "Failed to fetch switch state"}, status=response.status_code)



@protected_resource()
def set_switch_state(request, endpoint_id, state):    
    state_value = "255" if state == "ON" else "0"
    url = f'https://www.gthinkinventors.in/api/gthink/alexa/{endpoint_id}/{state_value}'
    response = requests.get(url)
    
    if response.status_code == 200:
        print(url, "url")
        print(state, "state")
        return JsonResponse({"state": state})
    else:
        return JsonResponse({"error": "Failed to set switch state"}, status=response.status_code)


@protected_resource()
def get_fan_speed(request, endpoint_id):
    print(request.user, "request.user")
    return JsonResponse({"speed": 10})


@protected_resource()
def set_fan_speed(request, endpoint_id, speed):
    print(speed, "speed")
    #devide it 25 and set
    return JsonResponse({"speed": 78})

