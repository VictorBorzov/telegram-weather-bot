from pyowm import OWM
from sys import path

path.append('modules')
from settings import get_owm_token

OPEN_WEATHER_TOKEN = get_owm_token()

owm = OWM(OPEN_WEATHER_TOKEN)
mgr = owm.weather_manager()

def weather_to_string(weather):
	tmp = weather.temperature('celsius')
	return "Temperature: {}°C\nFeels like: {}°C\nHumidity: {}%\nWind speed: {} m/sec\nPressure: {} hPa".format(
		tmp['temp'], tmp['feels_like'], weather.humidity, weather.wind()['speed'], weather.pressure["press"])
	
def get_weather_by_coordinates(lat, long):
    lat = float(lat)
    long = float(long)
    observation_list = mgr.weather_at_coords(lat, long)      
    return weather_to_string(observation_list.weather)

def get_weather_by_city_id(city_id):
    city_id = int(city_id)
    observation_list = mgr.weather_at_id(city_id)      
    return weather_to_string(observation_list.weather)
                
            