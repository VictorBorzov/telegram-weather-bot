from configparser import ConfigParser

config = ConfigParser()
config.read("config")

def get_bot_token():
	section = "Tokens"
	option = "Bot"
	if not config.has_option(section, option):
		raise ("config file doesn't contain {}:{}".format(section, option))
	return config[section][option]

def get_owm_token():
	section = "Tokens"
	option = "OpenWeatherMap"
	if not config.has_option(section, option):
		raise ("config file doesn't contain {}:{}".format(section, option))
	return config[section][option]
	