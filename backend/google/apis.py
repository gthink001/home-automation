from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@csrf_exempt
@api_view(['POST'])
def google_actions(request):
    try:
        request_data = request.data
        print(request_data)
        intent = request_data['inputs'][0]['intent']

        if intent == 'action.devices.SYNC':
            return sync()

        elif intent == 'action.devices.QUERY':
            return query(request_data)

        elif intent == 'action.devices.EXECUTE':
            return execute(request_data)

        elif intent == 'action.devices.DISCONNECT':
            return disconnect()

        else:
            return JsonResponse({"error": "Invalid intent"})

    except Exception as error:
        logger.error(error)
        JsonResponse({"error": str(error)})
        

def sync():
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
    devices = [get_endpoint_from_appliance(appliance) for appliance in appliances]
    devices = [device for device in devices if device is not None]

    response_data = {
        "requestId": "request_id",
        "payload": {
            "agentUserId": "agent_user_id",
            "devices": devices,
        },
    }
    print(response_data, "response_data")
    return JsonResponse(response_data)


def query(request_data):
    devices = request_data['inputs'][0]['payload']['devices']
    query_results = {}

    for device in devices:
        device_id = device['id']
        #device_id == "C44F330C30A5T1" needs to be changed, there must be a way to get device type from device_id
        if device_id == "C44F330C30A5T1":
            url = f'https://www.gthinkinventors.in/api/gthink/alexa_state/{device_id}'
            response = requests.get(url)
            if not response.status_code == 200:
                return JsonResponse({"error": "Failed to fetch switch state"}, status=response.status_code)

            state_data = response.json()
            state = True if state_data["State"] == "1" else False

            if state is not None:
                query_results[device_id] = {
                    "online": True,
                    "on": state
                }
        
        elif device_id == "840D8ED6A060F1":
            query_results[device_id] = {
                "online": True,
                "currentFanSpeedPercent": 50
            }

    response_data = {
        "requestId": request_data["requestId"],
        "payload": {
            "devices": query_results
        }
    }
    print(response_data, "response_data")
    return JsonResponse(response_data)



def execute(request_data):
    commands = request_data['inputs'][0]['payload']['commands']
    execution_results = []

    for command in commands:
        device_ids = [device['id'] for device in command['devices']]
        execution = command['execution'][0]

        for device_id in device_ids:
            if execution["command"] == "action.devices.commands.OnOff":
                state_value = "255" if execution["params"]["on"] else "0"
                url = f'https://www.gthinkinventors.in/api/gthink/alexa/{device_id}/{state_value}'
                response = requests.get(url)
                
                if not response.status_code == 200:
                    return JsonResponse({"error": "Failed to set switch state"}, status=response.status_code)

                execution_results.append({
                    "ids": [device_id],
                    "status": "SUCCESS",
                    "states": {
                        "online": True,
                        "on": state_value == "255"
                    }
                })
                    
            elif execution["command"] == "action.devices.commands.SetFanSpeedPercent":
                new_speed = execution["params"]["fanSpeedPercent"]
                #make a request to change fan speed
                if new_speed is not None:
                    execution_results.append({
                        "ids": [device_id],
                        "status": "SUCCESS",
                        "states": {
                            "online": True,
                            "currentFanSpeedPercent": new_speed
                        }
                    })

    response_data = {
        "requestId": request_data["requestId"],
        "payload": {
            "commands": execution_results
        }
    }

    return JsonResponse(response_data)


def disconnect():
    # Implement any necessary logic to clean up resources or revoke user access
    # In this example, no action is taken, and we return an empty JSON response

    return JsonResponse({})



def get_endpoint_from_appliance(appliance):
    if appliance["modelName"] == "Switch":
        return {
            "id": appliance["applianceId"],
            "type": "action.devices.types.SWITCH",
            "traits": ["action.devices.traits.OnOff"],
            "name": {"defaultNames": [appliance["friendlyName"]], "name": appliance["friendlyName"]},
            "willReportState": appliance["isReachable"],
        }
        
    elif appliance["modelName"] == "Fan":
        return {
            "id": appliance["applianceId"],
            "type": "action.devices.types.FAN",
            "traits": ["action.devices.traits.FanSpeed"],
            "name": {"defaultNames": [appliance["friendlyName"]], "name": appliance["friendlyName"]},
            "willReportState": appliance["isReachable"],
            "attributes": {
                "action.devices.traits.FanSpeed.supportedRanges": [
                    {
                        "minPercentSpeed": 0,
                        "maxPercentSpeed": 100,
                        "resolution": 1,
                        "ordered": True
                    }
                ],
                "reversible": False
            }
        }
    else:
        return None
    
