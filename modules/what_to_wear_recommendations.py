
def get_recomendations_by_weather(weather):
    recommendation = ""
    if weather.clouds < 20:
        recommendation += "\nIt should be sunny, so a hat or sunglasses might be needed."
    if weather.temperature('celsius')['temp'] < 0:
        if weather.temperature('celsius')['temp'] > -10:
            recommendation += "\nIt'll be frosty, so wear a coat, warm gloves and pants and don't forget about wool hat and scarf"        
        elif weather.temperature('celsius')['temp'] > -20:
            recommendation += "\nIt'll freezing so wear several layers of winter clothes"
        else:
            recommendation += "\nIt'll be colder than -20, so you should consider about staying inside"
    else:
        if weather.temperature('celsius')['temp'] < 10:
            recommendation += "\nIt'll be chilly, so consider a coat and autumn pants"                    
        elif weather.temperature('celsius')['temp'] < 20:
            recommendation += "\nIt'll be chilly, so consider a sweater and jeans"                    
        else:
            recommendation += "\nIt'll be hot, so consider a t-shirt and shorts"        
    if weather.wind()["speed"] > 6:
        recommendation += "\nThere'll be wind, so a jacket might be useful."
    elif weather.wind()["speed"] > 3:
        recommendation += "\nThere'll be a light breeze, so long sleeves might be useful."
    else:
        recommendation += "\nThe air will be quite calm, so no need to worry about wind."
    if not bool(weather.rain):
        recommendation += "\nIt's not going to rain, so no umbrella is needed."
    elif weather.rain['3h'] < 0.25:
        recommendation += "\nThere'll be light rain, so consider a hood or umbrella."
    elif weather.rain['3h'] < 0.5:
        recommendation += "\nThere'll be moderate rain, so an umbrella is probably needed."
    elif weather.rain['3h'] < 0.75:
        recommendation += "\nThere'll be heavy rain, so you'll need an umbrella and a waterproof top."
    elif weather.rain['3h'] < 1:
        recommendation += "\nThere'll be violent rain, so wear a life jacket."	
    return recommendation