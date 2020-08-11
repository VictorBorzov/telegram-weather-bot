from pyowm import OWM
import json

OPEN_WEATHER_TOKEN = "8b103e84d923cfbf598b64dec25e77ee"

def get_weather(lat, long):
    lat = float(lat)
    long = float(long)
    owm = OWM(OPEN_WEATHER_TOKEN)
    mgr = owm.weather_manager()
    observation_list = mgr.weather_at_coords(lat, long)      
    weather = observation_list.weather
    tmp = weather.temperature('celsius')
    return "temperature: {}, feels like: {}, humidity: {}, wind: {}, status: {}".format(tmp['temp'], tmp['feels_like'], weather.humidity, weather.wind()['speed'], weather.status)

def get_weather_by_city_id(city_id):
    city_id = int(city_id)
    owm = OWM(OPEN_WEATHER_TOKEN)
    mgr = owm.weather_manager()
    observation_list = mgr.weather_at_id(city_id)      
    weather = observation_list.weather
    tmp = weather.temperature('celsius')
    return "temperature: {}, feels like: {}, humidity: {}, wind: {}, status: {}".format(tmp['temp'], tmp['feels_like'], weather.humidity, weather.wind()['speed'], weather.status)
            
def safe_get_weather(lat, long):
    try:
        data = get_weather(lat, long)
        return True, data
    except:
        return False, "error while getting weather"
                
def get_cities():
    with open("data\city.list.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def safe_get_cities():
    try:
        data = get_cities()
        return True, data
    except:
        return False, "error while getting cities list"

