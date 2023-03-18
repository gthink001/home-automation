
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
    }
]



def fetch_appliances_service():
    #call django api and get list of appliances
    return SAMPLE_APPLIANCES


def fetch_device_state_service(endpoint_id, state):
    # Return the current state of the device, e.g. 'ON' or 'OFF'
    return "ON"


def set_device_state_service(endpoint_id, state, value):
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
    return False
