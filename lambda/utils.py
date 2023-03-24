
def get_name_from_capability(capability):
    """
    capability = {
            "interface": "Alexa.PowerController",
            "properties": {
                "proactivelyReported": true,
                "retrievable": true,
                "supported": [
                    {
                        "name": "powerState"
                    }
                ]
            },
            "type": "AlexaInterface",
            "version": "3"
        }
    """
    properties = capability.get("properties")
    if properties is not None:
        supported = properties.get("supported")
        if supported is not None and len(supported) > 0:
            name = supported[0].get("name", None)
            return name
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

        # elif model_name == 'Fan':
        #     capabilities = [
        #         {
        #             "type": "AlexaInterface",
        #             "interface": "Alexa.PercentageController",
        #             "version": "3",
        #             "properties": {
        #                 "supported": [
        #                     { "name": "percentage" }
        #                 ],
        #                 "proactivelyReported": True,
        #                 "retrievable": True
        #             }
        #         }
        #     ]

        elif model_name == 'Fan':
            capabilities = [
                {
                "type": "AlexaInterface",
                "interface": "Alexa.RangeController",
                "version": "3",
                "instance": "Fan.Speed",
                "properties": {
                    "supported": [
                        {
                            "name": "rangeValue"
                        }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                },
                "capabilityResources": {
                    "friendlyNames": [
                        {
                            "@type": "text",
                            "value": {
                                "text": "Fan speed",
                                "locale": "en-IN"
                            }
                        }
                    ]
                },
                "configuration": {
                    "supportedRange": {
                        "minimumValue": 0,
                        "maximumValue": 100,
                        "precision": 1
                    },
                    "unitOfMeasure": "Alexa.Unit.Percent"
                }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.PowerController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "powerState"
                  }
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
