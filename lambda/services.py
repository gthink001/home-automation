import requests
from utils import get_endpoint_from_appliance

BACKEND_BASE_URL = "https://af15-2405-201-2003-c828-16e8-7e68-3c7e-e7a4.in.ngrok.io"



def fetch_appliances_service(access_token):
    endpoints = []
    
    url = "{}/lambda/get_appliances".format(BACKEND_BASE_URL)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if not response.status_code == 200:
        logger.info("fetch_appliances_service response.status_code is not 200")
        return endpoints
   
    appliances = response.json()
    for appliance in appliances:
        endpoints.append(get_endpoint_from_appliance(appliance))
    return endpoints



def fetch_appliance_state_service(endpoint_id, access_token, namespace=None, name=None):
    if name == "powerState":
        # url = "{}/lambda/get_switch_state{}".format(BACKEND_BASE_URL, endpoint_id)
        # headers = {'Authorization': f'Bearer {access_token}'}
        # response = requests.get(url, headers=headers)

        # if not response.status_code == 200:
        #     logger.info("fetch_appliances_service response.status_code is not 200")
        #     return None
        # return response.json()
        return "ON"
    
    if namespace == 'Alexa.PercentageController':
        # url = "{}/lambda/get_fan_speed{}".format(BACKEND_BASE_URL, endpoint_id)
        # headers = {'Authorization': f'Bearer {access_token}'}
        # response = requests.get(url, headers=headers)

        # if not response.status_code == 200:
        #     logger.info("fetch_appliances_service response.status_code is not 200")
        #     return None
        return 50
    

def set_fan_speed_service(endpoint_id, access_token, state, value):
    return 50


def set_switch_state_service(endpoint_id, access_token, state, value):
    """
    call django api to set on off 
    """
    return True
