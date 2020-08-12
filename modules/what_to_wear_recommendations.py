
def get_recomendations_by_weather(weather):
	recommendation = ""
	if weather.clouds < 20:
		recommendation += "\nIt should be sunny, so a hat or sunglasses might be needed."

	if weather.wind()["speed"] > 6:
		recommendation += "\nThere'll be wind, so a jacket might be useful."
	elif weather.wind()["speed"] > 3:
		recommendation += "\nThere'll be a light breeze, so long sleeves might be useful."
	else:
		recommendation += "\nThe air will be quite calm, so no need to worry about wind."
	if not bool(weather.rain):
		recommendation += "\nIt's not going to rain, so no umbrella is needed."
	elif weather.rain['1h'] / 3 < 2.5:
		recommendation += "\nThere'll be light rain, so consider a hood or umbrella."
	elif weather.rain['1h'] / 3 < 7.6:
		recommendation += "\nThere'll be moderate rain, so an umbrella is probably needed."
	elif weather.rain['1h'] / 3 < 50:
		recommendation += "\nThere'll be heavy rain, so you'll need an umbrella and a waterproof top."
	elif weather.rain['1h'] / 3 > 50:
		recommendation += "\nThere'll be violent rain, so wear a life jacket."	
	return recommendation