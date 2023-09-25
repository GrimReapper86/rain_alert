import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

MY_LAT = 44.376308
My_LNG = 26.105206
api_url = 'https://api.openweathermap.org/data/3.0/onecall'
api_key = "b5430715a3ef9b7a546fba823df195fb"
account_sid = "ACb910bb57c93fc99052b72b37bc31b49c"
auth_token = "e9adb9d8c1b232654ef3f5d9f0e4b8f3"

parameters = {
    "lat": MY_LAT,
    "lon": My_LNG,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}
response = requests.get(url=api_url, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        from_='+12564725540',
        body='Bring your umbrella⛈️🌧️☂️',
        to='+40********'
    )

    print(message.status)
