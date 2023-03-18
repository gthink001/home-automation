from alexa_response import AlexaResponse
from validation import validate_message
from services import fetch_appliances_service, set_device_state_service, fetch_device_state_service

import logging
import time
import json
import uuid

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(request, context):
    # Dump the request for logging - check the CloudWatch logs
    logger.info("lambda_handler request:")
    logger.info(json.dumps(request, indent=4, sort_keys=True))

    if context is not None:
        logger.info("lambda_handler context:")
        logger.info(context)

    # Validate we have an Alexa directive
    if 'directive' not in request:
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(aer.get())


    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']


    if namespace == 'Alexa.Authorization':
        if name == 'AcceptGrant':
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request['directive']['payload']['grant']['code']
            grantee_token = request['directive']['payload']['grantee']['token']
            aar = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')
            return send_response(aar.get())


    if namespace == 'Alexa.Discovery':
        if name == 'Discover':
            adr = AlexaResponse(namespace='Alexa.Discovery', name='Discover.Response')
            adr.set_payload_endpoint = get_endpoints()
            return send_response(adr.get())



    if namespace == 'Alexa':
        if name == 'ReportState':
            
            endpoint_id = request['directive']['endpoint']['endpointId']
            power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
            correlation_token = request['directive']['header']['correlationToken']
            
            power_state_value = fetch_device_state_service(endpoint_id=endpoint_id, state='powerState')
                
            # Check for an error when getting the state
            if power_state_value is None:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint.'}).get()

            adr = AlexaResponse(namespace='Alexa', name='StateReport', correlation_token=correlation_token)
            adr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
            return send_response(adr.get())


    if namespace == 'Alexa.PowerController':
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        endpoint_id = request['directive']['endpoint']['endpointId']
        power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
        correlation_token = request['directive']['header']['correlationToken']

        # Check for an error when setting the state
        state_set = set_device_state_service(endpoint_id=endpoint_id, state='powerState', value=power_state_value)
        if not state_set:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint.'}).get()

        apcr = AlexaResponse(correlation_token=correlation_token)
        apcr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
        return send_response(apcr.get())



def send_response(response):
    # TODO Validate the response
    #validate_message(request, response)
    logger.info("lambda_handler response:")
    logger.info(json.dumps(response, indent=4, sort_keys=True))
    return response


def get_endpoints():
    endpoints = []
    appliances = fetch_appliances_service()
    for appliance in appliances:
        endpoints.append(get_endpoint_from_appliance(appliance))
    return endpoints


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


def get_display_categories(appliance):
    model_name = appliance["modelName"]
    if model_name == "Switch": displayCategories = ["SWITCH"]
    elif model_name == "Fan": displayCategories = ["FAN"]
    else: displayCategories = ["OTHER"]
    return displayCategories


def get_capabilities(appliance):
    model_name = appliance["modelName"]
    if model_name == 'Switch':
        capabilities = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PowerController",
                "version": "3",
                "properties": {
                    "supported": [
                        { "name": "powerState" }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                }
            }
        ]

    elif model_name == 'Fan':
        capabilities = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PercentageController",
                "version": "3",
                "properties": {
                    "supported": [
                        { "name": "percentage" }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                }
            }
        ]

    else:
        # in this example, just return simple on/off capability
        capabilities = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PowerController",
                "version": "3",
                "properties": {
                    "supported": [
                        { "name": "powerState" }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                }
            }
        ]

    # additional capabilities that are required for each endpoint
    endpoint_health_capability = {
        "type": "AlexaInterface",
        "interface": "Alexa.EndpointHealth",
        "version": "3",
        "properties": {
            "supported":[
                { "name":"connectivity" }
            ],
            "proactivelyReported": True,
            "retrievable": True
        }
    }
    alexa_interface_capability = {
        "type": "AlexaInterface",
        "interface": "Alexa",
        "version": "3"
    }
    capabilities.append(endpoint_health_capability)
    capabilities.append(alexa_interface_capability)
    return capabilities
