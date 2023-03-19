from django.http import JsonResponse
from oauth2_provider.decorators import protected_resource


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
    print(request.user, "request.user")
    
    return JsonResponse()


@protected_resource()
def set_switch_state(request, endpoint_id, state):
    print(request.user, "request.user")
    
    return JsonResponse()


@protected_resource()
def get_fan_speed(request, endpoint_id):
    print(request.user, "request.user")
    
    return JsonResponse(appliances, safe=False)


@protected_resource()
def set_fan_speed(request, endpoint_id, speed):
    print(request.user, "request.user")
    
    return JsonResponse(appliances, safe=False)

