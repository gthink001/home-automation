https://django-allauth.readthedocs.io/en/latest/configuration.html

https://docs.google.com/document/d/14gG-QGWtyFainvmcuI2jY8U2ADwnrWCm_BNpNY6ikp4/edit

Username: viraj.megrut@gmail.com
Email address: viraj.megrut@gmail.com
#viraz@171198


Client id django app
1BmHnKQqFJhWE1ATtX67rx8CNrcSsNpc0XeCQsI4

Secret django app
jQriMFeTrMAJtdfUsUGptjWBrMMTYptfc29V0epnZq5UjREvxEkm5PH8tZ2yQsonfI44zoT3XZtQdaMa2GkDxq5vj97AQXkHRXPg1KoB6k0glVOEjXu1zQImV1WYkvYF



http://127.0.0.1:8000/o/authorize/?client_id=1BmHnKQqFJhWE1ATtX67rx8CNrcSsNpc0XeCQsI4&response_type=code&redirect_uri=http://localhost:8000/callback&state=local&scope=alexa

code=KWL6OrTRFFkwcUvxmJ02zXG4hgwhmu

POST https://your-domain.com/o/token/

Headers:
Content-Type: application/x-www-form-urlencoded

Body:
grant_type=authorization_code
&code=YOUR_AUTHORIZATION_CODE
&redirect_uri=YOUR_REDIRECT_URI
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET



Directive: when connected 
{
    "directive": {
        "header": {
            "messageId": "1f65000b-9bf2-4724-a596-e5b79e73e62a",
            "name": "Discover",
            "namespace": "Alexa.Discovery",
            "payloadVersion": "3"
        },
        "payload": {
            "scope": {
                "token": "K9RSWZ0uHYFY0jaN03N3RL0L34zVSi",
                "type": "BearerToken"
            }
        }
    }
}



endpoints: SAMPLE_APPLIANCES for v3
[
    {
    "capabilities": [
        {
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
        },
        {
            "interface": "Alexa.EndpointHealth",
            "properties": {
                "proactivelyReported": true,
                "retrievable": true,
                "supported": [
                    {
                        "name": "connectivity"
                    }
                ]
            },
            "type": "AlexaInterface",
            "version": "3"
        },
        {
            "interface": "Alexa",
            "type": "AlexaInterface",
            "version": "3"
        }
    ],
    "cookie": {},
    "description": "001 Switch that can only be turned on/off",
    "displayCategories": [
        "OTHER"
    ],
    "endpointId": "C44F330C30A5T1",
    "friendlyName": "Switch",
    "manufacturerName": "G-Think"
},
    {
    "capabilities": [
        {
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
        },
        {
            "interface": "Alexa.EndpointHealth",
            "properties": {
                "proactivelyReported": true,
                "retrievable": true,
                "supported": [
                    {
                        "name": "connectivity"
                    }
                ]
            },
            "type": "AlexaInterface",
            "version": "3"
        },
        {
            "interface": "Alexa",
            "type": "AlexaInterface",
            "version": "3"
        }
    ],
    "cookie": {},
    "description": "002 fan",
    "displayCategories": [
        "OTHER"
    ],
    "endpointId": "840D8ED6A060F1",
    "friendlyName": "Fan",
    "manufacturerName": "G-Think"
}
]



response to discovery 
[INFO]	2023-03-18T18:30:54.295Z	2dda9d4b-8a54-4ae8-a72a-1a4823807e28	{
    "event": {
        "header": {
            "messageId": "99e9ad85-4c08-4c0c-b25f-286397e082d9",
            "name": "Discover.Response",
            "namespace": "Alexa.Discovery",
            "payloadVersion": "3"
        },
        "payload": {
            "endpoints": [
                {
                    "capabilities": [
                        {
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
                        },
                        {
                            "interface": "Alexa.EndpointHealth",
                            "properties": {
                                "proactivelyReported": true,
                                "retrievable": true,
                                "supported": [
                                    {
                                        "name": "connectivity"
                                    }
                                ]
                            },
                            "type": "AlexaInterface",
                            "version": "3"
                        },
                        {
                            "interface": "Alexa",
                            "type": "AlexaInterface",
                            "version": "3"
                        }
                    ],
                    "cookie": {},
                    "description": "001 Switch that can only be turned on/off",
                    "displayCategories": [
                        "OTHER"
                    ],
                    "endpointId": "C44F330C30A5T1",
                    "friendlyName": "Switch",
                    "manufacturerName": "G-Think"
                },
                {
                    "capabilities": [
                        {
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
                        },
                        {
                            "interface": "Alexa.EndpointHealth",
                            "properties": {
                                "proactivelyReported": true,
                                "retrievable": true,
                                "supported": [
                                    {
                                        "name": "connectivity"
                                    }
                                ]
                            },
                            "type": "AlexaInterface",
                            "version": "3"
                        },
                        {
                            "interface": "Alexa",
                            "type": "AlexaInterface",
                            "version": "3"
                        }
                    ],
                    "cookie": {},
                    "description": "002 fan",
                    "displayCategories": [
                        "OTHER"
                    ],
                    "endpointId": "840D8ED6A060F1",
                    "friendlyName": "Fan",
                    "manufacturerName": "G-Think"
                }
            ]
        }
    }
}





status request 
{
    "directive": {
        "endpoint": {
            "cookie": {},
            "endpointId": "endpoint-002",
            "scope": {
                "token": "K9RSWZ0uHYFY0jaN03N3RL0L34zVSi",
                "type": "BearerToken"
            }
        },
        "header": {
            "correlationToken": "AAAAAAAAAQCZOPdm8Zg9ZpLaxteB61dJAAIAAAAAAACbOrXuUpMCxKztRTqLWo/UXK+wNYgIaQ8VUqRxGWF3MdmgJbCkxJ/51YBXSUXvoKso55DRIy2W7tPxYZ/eRHpxLAr2LtiYssk0BRNaKvQvDIJgLMKE1eWFVbFBfUhS1OFPKf68PlY+CSgTL8S+XSmm43ljb614j2MU3xkfocecYs1U8KyAUBa025ApYRI403t0Gd8SNSiO2R9PcmoynhcOIWbvy2Qx0DhPaFpkTIIZj6dGsnP0FtWSzdMzjJdS5c6hKpD2ska7HfY04tVRioFOtUa7vMwF1kpGQSge6/TDsmA4pFj0VFpk+FlcN+mkUIONDPD7iMSJkBgxcOC01amFB1nDTiW23tiigQzdcWNqP2w57abO0uZgTX6GIZZ0hqt8GurP18ywLSHLaQagjiIR4MoKYZDAY4d/itmKOh7a5y40yBvAHuTnmYBTyLJndRp+JoYDx0hrUb3+hyY8rThmNYOlmAsY8p1A3ovM8gDwWRtusUt80SWJsjodjRJTCafRIglItX6KBjgzCUWtCuI36SGK4G2/rgjByh84XSAaLC+w3J0HuCqYaDYv2mcMkHM/NgL/ASd8MlXrYhok+Q1Vry+5B2Gzy8gOEoCgVsYJurX+uQqqINCmszILhk++1Wq63fJzq0adCoVArgoPDnZX+bxk5HqWb+yF76wJH+EBZw==",
            "messageId": "73828507-d7b2-400f-8b4c-7abb9314a8b4",
            "name": "ReportState",
            "namespace": "Alexa",
            "payloadVersion": "3"
        },
        "payload": {}
    }
}
