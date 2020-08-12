# Smart weather forecaster
This service is implemented as a telegram bot in python 3.8.0
* telegram bot framework - aiogram
* weather forecast framework - pyowm

## Descripition:
The user shares location data (the telegram desktop application does not support this feature, in this case, you must select a country and city).   
The service requests the weather 3 day forecast (for every 3 hour in a day) for the selected location and sends a formatted response:
> Date and time  
> General status: [sunny]  
> Temperature: [  ] °C  
> Feels like: [  ] °C  
> Humidity: [  ] %  
> Wind speed: [  ] m/s  
> Pressure: [  ] hPa  
> Recommendations for what to wear: [ ] 

## How it works
The user has two branches of dialogue with the telegram bot to select a location for the weather forecast: through the selection of the city and through the location request.

Branch with a city selection:
1. The user enters the country code. Tere is a command to print the available codes.
2. The user enters the name of the city. There is a command to display available names with the chat keyboard.
3. The user specifies the city coordinates if the database contains several cities in the selected country with the selected name.

The database is the json file loaded from OpenWeatherMap.org
In the second dialogue branch user just shares his location.
The bot requests the weather forecast by the city id or by the coordinates and generates recommendations for the given conditions and sends a series of messages with a forecast for 3 days (for every 3h).

## How to use
1. Clone repo 
2. Register your telegram bot https://t.me/botfather */newbot*
3. Sign up and get API key on https://openweathermap.org/home/sign_up
4. Add tokens to the config file
5. Install requirements
```sh
$ pip install -r requirements.txt
```
4. Start bot
```sh
$ python bot.py
```
5. Use your teleram bot to get forecasts
