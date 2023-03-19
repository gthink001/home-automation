
SAMPLE_APPLIANCES = [
    # {
    #     "applianceId": "C44F330C30A5T1",
    #     "manufacturerName": "G-Think",
    #     "modelName": "Switch",
    #     "version": "1",
    #     "friendlyName": "Switch",
    #     "friendlyDescription": "001 Switch that can only be turned on/off",
    #     "isReachable": True,
    #     "actions": [
    #         "turnOn",
    #         "turnOff"
    #     ],
    #     "additionalApplianceDetails": {
    #     }
    # },
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
    }
]


def fetch_appliances_from_api():
    """
    call django api here
    """
    return SAMPLE_APPLIANCES


def fetch_appliances_service():
    endpoints = []
    appliances = fetch_appliances_from_api()
    for appliance in appliances:
        endpoints.append(get_endpoint_from_appliance(appliance))
    return endpoints


def get_appliance_by_appliance_id(appliance_id):
    for appliance in SAMPLE_APPLIANCES:
        if appliance["applianceId"] == appliance_id:
            return appliance
    return None

def get_endpoint_from_appliance(appliance):

    def _get_display_categories(appliance):
        model_name = appliance["modelName"]
        if model_name == "Switch": displayCategories = ["SWITCH"]
        elif model_name == "Fan": displayCategories = ["FAN"]
        else: displayCategories = ["OTHER"]
        return displayCategories

    def _get_capabilities(appliance):
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

    endpoint = {
        "endpointId": appliance["applianceId"],
        "manufacturerName": appliance["manufacturerName"],
        "friendlyName": appliance["friendlyName"],
        "description": appliance["friendlyDescription"],
        "displayCategories": [],
        "cookie": appliance["additionalApplianceDetails"],
        "capabilities": []
    }
    endpoint["displayCategories"] = _get_display_categories(appliance)
    endpoint["capabilities"] = _get_capabilities(appliance)
    return endpoint


def fetch_appliance_state_service(endpoint_id, namespace, name):
    if name == "powerState":
        return "ON" / "OFF"
    
    if name == "percentage":
        return 45


def set_fan_speed_service(endpoint_id, state, value):
    return 50

def set_switch_state_service(endpoint_id, state, value):
    """
    call django api to set on off 
    """
    # attribute_key = state + 'Value'
    # response = aws_dynamodb.update_item(
    #     TableName='SampleSmartHome',
    #     Key={'ItemId': {'S': endpoint_id}},
    #     AttributeUpdates={attribute_key: {'Action': 'PUT', 'Value': {'S': value}}})
    # print(response)
    # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    #     return True
    # else:
    return True
