from pyowm import OWM
from sys import path

path.append('modules')
from settings import get_owm_token

OPEN_WEATHER_TOKEN = get_owm_token()
owm = OWM(OPEN_WEATHER_TOKEN)
mgr = owm.weather_manager()

def weather_to_string(weather):
	tmp = weather.temperature('celsius')
	return "In general: {}\nTemperature: {}°C\nFeels like: {}°C\nHumidity: {}%\nWind speed: {} m/sec\nPressure: {} hPa".format(
		weather.status, tmp['temp'], tmp['feels_like'], weather.humidity, weather.wind()['speed'], weather.pressure["press"])

def forecast_to_string(forecast):
	return map(lambda weather : weather.reference_time('iso') + "\n" + weather_to_string(weather), forecast.weathers[:16])
	
def get_weather_by_coordinates(lat, long):
    lat = float(lat)
    long = float(long)
    observation_list = mgr.weather_at_coords(lat, long)      
    return weather_to_string(observation_list.weather)

def get_weather_by_city_id(city_id):
    city_id = int(city_id)
    observation_list = mgr.weather_at_id(city_id)      
    return weather_to_string(observation_list.weather)
                            
def get_3h_forecast_by_coordinates(lat, long):
	lat = float(lat)
	long = float(long)
	forecast = mgr.forecast_at_coords(lat, long, "3h").forecast     
	return forecast_to_string(forecast)

def get_3h_forecast_by_city_id(city_id):
    city_id = int(city_id)
    forecast = mgr.forecast_at_id(city_id, "3h").forecast    
    return forecast_to_string(forecast)
import what_to_wear_recommendations as rec                            							
weather = mgr.weather_at_id(524894).weather
print(rec.get_recomendations_by_weather(weather))
