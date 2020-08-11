import telebot
import requests
import json


BOT_TOKEN = '1319888554:AAHq87K4FeErNJM63HdqANzlOfeDHk3O-2k'
    

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
    
@bot.message_handler(commands=['weather'])    
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
    
@bot.message_handler(commands=['cities'])    
def send_welcome(message):
	bot.reply_to(message, get_cities())    