from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp
from sys import path

path.append('modules')
import open_weather_api as owa
    
class GPSDetection(StatesGroup):
	waiting_for_location = State()
	waiting_for_weather_by_coords = State()
    
@dp.message_handler(commands="weather_by_gps", state="*")
async def gps_detection_step_1(message: types.Message):	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	button = types.KeyboardButton(text="Share location", request_location=True)
	keyboard.add(button)
	await message.answer("Please, share yout location", reply_markup=keyboard)
	await GPSDetection.waiting_for_location.set()
	
@dp.message_handler(state=GPSDetection.waiting_for_location, content_types=types.ContentTypes.LOCATION)
async def gps_detection_step_1(message: types.Message):	
	forecast = owa.get_3h_forecast_by_coordinates(message.location.latitude, message.location.longitude)
	for weather in forecast:
		await message.answer(weather)	
