import requests
from twilio.rest import Client
import os

URL = "https://api.openweathermap.org/data/3.0/onecall"
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

api_key = os.environ.get("API_KEY")

parameters = {
    "lat": -1.234576,
    "lon": 36.931899,
    # "exclude": "current,minutely,daily",
    "appid": api_key,

}

response = requests.get(URL, params=parameters)
response.raise_for_status()

weather_data = response.json()

# weather conditions in 12 hours daytime
daytime_weather = weather_data["hourly"][:12]

will_rain = False

for hourly_data in daytime_weather:
    weather_condition = hourly_data["weather"][0]["id"]
    if int(weather_condition) < 600:
        will_rain = True

# Notify user via sms
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_='+12569739894',
        to='+254716517329'
    )

    print(message.status)
