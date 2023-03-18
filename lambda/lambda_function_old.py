# -*- coding: utf-8 -*-

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""Alexa Smart Home Lambda Function Sample Code.

This file demonstrates some key concepts when migrating an existing Smart Home skill Lambda to
v3, including recommendations on how to transfer endpoint/appliance objects, how v2 and vNext
handlers can be used together, and how to validate your v3 responses using the new Validation
Schema.

Note that this example does not deal with user authentication, only uses virtual devices, omits
a lot of implementation and error handling to keep the code simple and focused.
"""

import logging
import time
import json
import uuid

# Imports for v3 validation
from validation import validate_message

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# To simplify this sample Lambda, we omit validation of access tokens and retrieval of a specific
# user's appliances. Instead, this array includes a variety of virtual appliances in v2 API syntax,
# and will be used to demonstrate transformation between v2 appliances and v3 endpoints.
SAMPLE_APPLIANCES = [
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
        "isReachable": true,
        "actions": [
            "setPercentage"
        ],
        "additionalApplianceDetails": {}
    },
    # {
    #     "applianceId": "endpoint-003",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart White Light",
    #     "version": "1",
    #     "friendlyName": "White Light",
    #     "friendlyDescription": "003 Light that is dimmable and can change color temperature only",
    #     "isReachable": True,
    #     "actions": [
    #         "turnOn",
    #         "turnOff",
    #         "setPercentage",
    #         "incrementPercentage",
    #         "decrementPercentage",
    #         "setColorTemperature",
    #         "incrementColorTemperature",
    #         "decrementColorTemperature"
    #     ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-004",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Thermostat",
    #     "version": "1",
    #     "friendlyName": "Thermostat",
    #     "friendlyDescription": "004 Thermostat that can change and query temperatures",
    #     "isReachable": True,
    #     "actions": [
    #         "setTargetTemperature",
    #         "incrementTargetTemperature",
    #         "decrementTargetTemperature",
    #         "getTargetTemperature",
    #         "getTemperatureReading"
    #     ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-004-1",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Thermostat Dual",
    #     "version": "1",
    #     "friendlyName": "Living Room Thermostat",
    #     "friendlyDescription": "004-1 Thermostat that can change and query temperatures, supports dual setpoints",
    #     "isReachable": True,
    #     "actions": [
    #         "setTargetTemperature",
    #         "incrementTargetTemperature",
    #         "decrementTargetTemperature",
    #         "getTargetTemperature",
    #         "getTemperatureReading"
    #     ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-005",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Lock",
    #     "version": "1",
    #     "friendlyName": "Lock",
    #     "friendlyDescription": "005 Lock that can be locked and can query lock state",
    #     "isReachable": True,
    #     "actions": [
    #         "setLockState",
    #         "getLockState"
    #     ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-006",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Scene",
    #     "version": "1",
    #     "friendlyName": "Good Night Scene",
    #     "friendlyDescription": "006 Scene that can only be turned on",
    #     "isReachable": True,
    #     "actions": [
    #         "turnOn"
    #     ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-007",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Activity",
    #     "version": "1",
    #     "friendlyName": "Watch TV",
    #     "friendlyDescription": "007 Activity that runs sequentially that can be turned on and off",
    #     "isReachable": True,
    #     "actions": [
    #         "turnOn",
    #         "turnOff"
    #         ],
    #     "additionalApplianceDetails": {}
    # },
    # {
    #     "applianceId": "endpoint-008",
    #     "manufacturerName": "Sample Manufacturer",
    #     "modelName": "Smart Camera",
    #     "version": "1",
    #     "friendlyName": "Baby Camera",
    #     "friendlyDescription": "008 Camera that streams from an RSTP source",
    #     "isReachable": True,
    #     "actions": [
    #         "retrieveCameraStreamUri"
    #         ],
    #     "additionalApplianceDetails": {}
    # }
]

def lambda_handler(request, context):
    """Main Lambda handler.

    Since you can expect both v2 and v3 directives for a period of time during the migration
    and transition of your existing users, this main Lambda handler must be modified to support
    both v2 and v3 requests.
    """

    try:
        logger.info("Directive:")
        logger.info(json.dumps(request, indent=4, sort_keys=True))

        version = get_directive_version(request)

        if version == "3":
            logger.info("Received v3 directive!")
            if request["directive"]["header"]["name"] == "Discover":
                response = handle_discovery(request)
            else:
                response = handle_non_discovery(request)

        logger.info("Response:")
        logger.info(json.dumps(response, indent=4, sort_keys=True))

        #if version == "3":
            #logger.info("Validate v3 response")
            #validate_message(request, response)

        return response
    except ValueError as error:
        logger.error(error)
        raise


def get_appliance_by_appliance_id(appliance_id):
    for appliance in SAMPLE_APPLIANCES:
        if appliance["applianceId"] == appliance_id:
            return appliance
    return None

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())


def handle_discovery(request):
    endpoints = []
    for appliance in SAMPLE_APPLIANCES:
        endpoints.append(get_endpoint_from_appliance(appliance))
    logger.info("endpoints:")
    logger.info(json.dumps(endpoints, indent=4, sort_keys=True))

    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": get_uuid()
            },
            "payload": {
                "endpoints": endpoints
            }
        }
    }
    return response

def handle_non_discovery(request):
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]

    if request_namespace == "Alexa.PowerController":
        if request_name == "TurnOn":
            value = "ON"
        else:
            value = "OFF"

        response = {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.PowerController",
                        "name": "powerState",
                        "value": value,
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": get_uuid(),
                    "correlationToken": request["directive"]["header"]["correlationToken"]
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": "access-token-from-Amazon"
                    },
                    "endpointId": request["directive"]["endpoint"]["endpointId"]
                },
                "payload": {}
            }
        }
        return response

    elif request_namespace == "Alexa.Authorization":
        if request_name == "AcceptGrant":
            response = {
                "event": {
                    "header": {
                        "namespace": "Alexa.Authorization",
                        "name": "AcceptGrant.Response",
                        "payloadVersion": "3",
                        "messageId": "5f8a426e-01e4-4cc9-8b79-65f8bd0fd8a4"
                    },
                    "payload": {}
                }
            }
            return response

    # other handlers omitted in this example


def get_endpoint_from_appliance(appliance):
    endpoint = {
        "endpointId": appliance["applianceId"],
        "manufacturerName": appliance["manufacturerName"],
        "friendlyName": appliance["friendlyName"],
        "description": appliance["friendlyDescription"],
        "displayCategories": [],
        "cookie": appliance["additionalApplianceDetails"],
        "capabilities": []
    }
    endpoint["displayCategories"] = get_display_categories(appliance)
    endpoint["capabilities"] = get_capabilities(appliance)
    return endpoint

def get_directive_version(request):
    try:
        return request["directive"]["header"]["payloadVersion"]
    except:
        try:
            return request["header"]["payloadVersion"]
        except:
            return "-1"

def get_endpoint_by_endpoint_id(endpoint_id):
    appliance = get_appliance_by_appliance_id(endpoint_id)
    if appliance:
        return get_endpoint_from_appliance(appliance)
    return None

def get_display_categories(appliance):
    model_name = appliance["modelName"]
    if model_name == "Switch": displayCategories = ["SWITCH"]
    elif model_name == "Fan": displayCategories = ["FAN"]
    # elif model_name == "Smart Light": displayCategories = ["LIGHT"]
    # elif model_name == "Smart Thermostat": displayCategories = ["THERMOSTAT"]
    # elif model_name == "Smart Lock": displayCategories = ["SMARTLOCK"]
    # elif model_name == "Smart Scene": displayCategories = ["SCENE_TRIGGER"]
    # elif model_name == "Smart Activity": displayCategories = ["ACTIVITY_TRIGGER"]
    # elif model_name == "Smart Camera": displayCategories = ["CAMERA"]
    else: displayCategories = ["OTHER"]
    return displayCategories
