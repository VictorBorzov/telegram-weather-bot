import sys
import telebot
import json 
from telebot import types
import open_weather_api as ow

TOKEN = '1319888554:AAHq87K4FeErNJM63HdqANzlOfeDHk3O-2k'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'weather'     : 'Get city weather',
    'countries'   : 'Show available countries',
    'cities'      : 'Show available cities for country'
}
   
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0  
    
# console output 
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
   
bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

# get list of cities from OpenWeatherMap
cities = ow.get_cities()

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hi, let's make some broadcasting here...")
        bot.send_message(cid, "Scanning complete, I know you now")
    command_help(m)  # show the new user the help page
    
# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# user can get a weather (multi-stage command)
@bot.message_handler(commands=['weather'])
def command_weather(m):
    cid = m.chat.id
    country_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the country selection keyboard
    country_processed = set()
    for city in cities:
        if not city['country'] in country_processed:
            country_processed.add(city['country'])
            country_select.add(city['country'])
    bot.send_message(cid, "Please choose your country", reply_markup=country_select)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)
    
# user can print available countries 
@bot.message_handler(commands=['countries'])
def command_countries(m):
    cid = m.chat.id
    country_processed = set()
    for city in cities:
        if not city['country'] in country_processed:
            country_processed.add(city['country'])
            bot.send_message(cid, city['country'])

# user can print available countries 
@bot.message_handler(commands=['cities'])
def command_cities(m):
    cid = m.chat.id
    country_processed = set()
    for city in cities:
        if not city['country'] in country_processed:
            country_processed.add(city['country'])
            bot.send_message(cid, city['country'])

# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_city_select(m):
    cid = m.chat.id
    country = m.text
    country_cities = [[city["name"], city["coord"]["lat"], city["coord"]["lon"]] for city in cities if city["country"] == country]
    if len(country_cities) == 0:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")
    else:
        city_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the country selection keyboard
        for city in country_cities:
            city_select.add('"name" : "{}", "lat" : "{}", "long" : "{}"'.format(city[0], city[1], city[2]))
        bot.send_message(cid, "Please choose your city", reply_markup=city_select)  # show the keyboard
        userStep[cid] = 2  # set the user to the next step (expecting a reply in the listener now)            

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def msg_get_weather(m):
    cid = m.chat.id
    text = "{" + m.text + "}"
    print(text)
    selected_city = json.loads(text)
    weather = ow.get_weather(float(selected_city["lat"]), float(selected_city["long"]))   
    bot.send_message(cid, weather)
    userStep[cid] = 0

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()