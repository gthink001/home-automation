# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

# from services import *
# from utils import get_name_from_capability

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@csrf_exempt
@api_view(['POST'])
def google_actions(request):
    try:
        request_data = json.loads(request.body)
        print(request_data, "request_data")
        intent = request_data['handler']['name']

        # Extract access token from the request
        access_token = request_data['user'].get('accessToken')

        if access_token is None:
            logger.warning("Access token not found in the request.")

        if intent == 'Discover':
            # Replace with your actual intent name for discovery
            adr = {
                'payload': {
                    'devices': fetch_appliances_service(access_token=access_token)
                }
            }
            return JsonResponse(adr)

        elif intent in ['TurnOn', 'TurnOff']:
            # Replace with your actual intent names for turning on and off
            endpoint_id = request_data['inputs'][0]['payload']['deviceId']
            power_state_value = 'OFF' if intent == 'TurnOff' else 'ON'

            state_set = set_switch_state_service(
                endpoint_id=endpoint_id,
                access_token=access_token,
                value=power_state_value
            )

            if not state_set:
                response = {
                    'status': 'ERROR',
                    'errorCode': 'endpointUnreachable',
                    'message': 'Unable to reach endpoint database.'
                }
            else:
                response = {
                    'status': 'SUCCESS'
                }
            return JsonResponse(response)

        # Add other intents and their respective handling as needed

    except Exception as error:
        logger.error(error)
        raise
