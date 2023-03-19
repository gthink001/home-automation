from alexa_response import AlexaResponse
from validation import validate_message
from services import *
from utils import get_name_from_capability

import logging
import time
import json
import uuid

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(request, context):
    # Dump the request for logging - check the CloudWatch logs
    try:
        logger.info("handler request:")
        logger.info(json.dumps(request, indent=4, sort_keys=True))

        if context is not None:
            logger.info("handler context:")
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
                adr.set_payload_endpoint(fetch_appliances_service())
                return send_response(adr.get())


        if namespace == 'Alexa':
            if name == 'ReportState':
                endpoint_id = request['directive']['endpoint']['endpointId']
                correlation_token = request['directive']['header']['correlationToken']
                
                appliances = fetch_appliances_service()
                
                for appliance in appliances:
                    if not appliance["endpointId"] == endpoint_id:
                        continue
            
                    adr = AlexaResponse(namespace='Alexa', name='StateReport', correlation_token=correlation_token)
                    capabilities = appliance.get("capabilities", [])
                    for capability in capabilities:
                        namespace = capability.get("interface")
                        name = get_name_from_capability.get(capability)
                        value = fetch_appliance_state_service(endpoint_id=endpoint_id, namespace=namespace, name=name)

                        # Check for an error when getting the state
                        if value is None:
                            continue
                            # return AlexaResponse(
                            #     name='ErrorResponse',
                            #     payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint.'}).get()

                        adr.add_context_property(namespace=namespace, name=name, value=value)
                    return send_response(adr.get())


        if namespace == 'Alexa.PowerController':
            # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
            endpoint_id = request['directive']['endpoint']['endpointId']
            power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
            correlation_token = request['directive']['header']['correlationToken']

            # Check for an error when setting the state
            state_set = set_switch_state_service(endpoint_id=endpoint_id, state='powerState', value=power_state_value)
            if not state_set:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

            apcr = AlexaResponse(correlation_token=correlation_token)
            apcr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
            return send_response(apcr.get())


        if namespace == 'Alexa.PercentageController':
            endpoint_id = request['directive']['endpoint']['endpointId']
            correlation_token = request['directive']['header']['correlationToken']

            if name == 'SetPercentage':
                fan_speed_value = request['directive']['payload']['percentage']
            elif name == 'AdjustPercentage':
                fan_speed_value = fetch_fan_speed_service(endpoint_id=endpoint_id)
                fan_speed_value += request['directive']['payload']['percentageDelta']
                fan_speed_value = max(min(fan_speed_value, 100), 0)

            # Check for an error when setting the state
            state_set = set_fan_speed_service(endpoint_id=endpoint_id, state='percentage', value=fan_speed_value)
            if not state_set:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

            apcr = AlexaResponse(correlation_token=correlation_token)
            apcr.add_context_property(
                namespace='Alexa.PercentageController', 
                name='percentage', 
                value=fan_speed_value, 
                uncertainty_in_milliseconds=500
            )
            return send_response(apcr.get())


    except Exception as error:
        logger.error(error)
        raise


def send_response(response):
    # TODO Validate the response
    #validate_message(request, response)
    logger.info("handler response:")
    logger.info(json.dumps(response, indent=4, sort_keys=True))
    return response
