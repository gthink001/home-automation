https://django-allauth.readthedocs.io/en/latest/configuration.html

https://docs.google.com/document/d/14gG-QGWtyFainvmcuI2jY8U2ADwnrWCm_BNpNY6ikp4/edit

Username: viraj.megrut@gmail.com
Email address: viraj.megrut@gmail.com
#viraz@171198


http://127.0.0.1:8000/o/authorize/?client_id=1BmHnKQqFJhWE1ATtX67rx8CNrcSsNpc0XeCQsI4&response_type=code&redirect_uri=http://localhost:8000/callback&state=YOUR_STATE_VALUE&scope=alexa

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