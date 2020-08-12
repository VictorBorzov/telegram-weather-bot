from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp
from string import ascii_uppercase
import json 
from sys import path

path.append('modules')
import open_weather_api as owa

with open("data\city.list.json", 'r', encoding="utf-8") as json_file:
    available_cities = json.load(json_file)
available_countries = set()
countries_to_cities = {}
for city in available_cities:
    if not city["country"]:
        continue
    if not city["country"] in available_countries:
        available_countries.add(city["country"])
        countries_to_cities[city["country"]] = []
    countries_to_cities[city["country"]].append(city)
available_countries = sorted(available_countries)

def find_cities_in_country(city_name, country_name):
    result = []
    for city in countries_to_cities[country_name]:
        if city["name"] == city_name:
            result.append(city)
    return result
    
class CityChoice(StatesGroup):
    waiting_for_country_name = State()
    waiting_for_city_id = State()
    
@dp.message_handler(commands="available_countries", state=CityChoice.waiting_for_country_name)
async def show_available_countries(message: types.Message):
    await message.answer(", ".join(available_countries))

# Yield successive n-sized 
# chunks from l. 
def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  
@dp.message_handler(commands="available_cities", state=CityChoice.waiting_for_city_id)
async def show_available_cities(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for c in ascii_uppercase:
        keyboard.add(c)
    await message.answer("Please, type first letter", reply_markup=keyboard)
    

# choose country 
@dp.message_handler(commands="weather_by_city", state="*")
async def city_step_1(message: types.Message):
    await message.answer("Choose country code: /available_countries")
    await CityChoice.waiting_for_country_name.set()

# choose city name
@dp.message_handler(state=CityChoice.waiting_for_country_name, content_types=types.ContentTypes.TEXT)
async def city_step_2(message: types.Message, state: FSMContext):  
    if message.text not in available_countries:
        await message.reply("Please, choose correct country code /available_countries.")
        return
    await state.update_data(chosen_country=message.text)
    await CityChoice.waiting_for_city_id.set()

    await message.reply("Please, choose city name /available_cities.")

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
	

# clarify city id if necessary
@dp.message_handler(state=CityChoice.waiting_for_city_id, content_types=types.ContentTypes.TEXT)
async def city_step_3(message: types.Message, state: FSMContext): 
	# show hint for first uppercase letter
	cities = set()
	user_data = await state.get_data()
	if message.text in ascii_uppercase:
		for city in countries_to_cities[user_data["chosen_country"]]:
			if not city["name"] in cities and city["name"][0] == message.text:
				cities.add(city["name"])
		cities = sorted(cities)
		splitted_cities = divide_chunks(list(cities), 100)
		for cities in splitted_cities:
			await message.answer(", ".join(cities))
		return

	if "id: " in message.text:
		id_str = message.text.split("id: ", 1)[1]
		if not RepresentsInt(id_str):
			await message.reply("Please, choose correct city name /available_cities.")
			return    
		#city id clarified            
		forecast = owa.get_3h_forecast_by_city_id(id_str)
		for weather in forecast:
			await message.answer(weather)	
		await state.finish()
		return 
	chosen_city_name = message.text    
	cities_with_name = find_cities_in_country(chosen_city_name, user_data["chosen_country"])
	if len(cities_with_name) < 1:
		await message.reply("Please, choose correct city name /available_cities.")
		return
	elif len(cities_with_name) > 1:
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
		for city in cities_with_name:
			keyboard.add("name: {}, latitude: {}, longitude: {}, id: {}".format(city["name"], city["coord"]["lat"], city["coord"]["lon"], city["id"]))
		await message.reply("Several cities found, please, clarify the location.", reply_markup=keyboard)
		return
	# city name is unique
	forecast = owa.get_3h_forecast_by_city_id(cities_with_name[0]["id"])
	for weather in forecast:
		await message.answer(weather)	
	await state.finish()

