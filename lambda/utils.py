
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