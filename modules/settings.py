from configparser import ConfigParser

config = ConfigParser()
config.read("config")

def get_bot_token():
	section = "Tokens"
	option = "Bot"
	if not config.has_option(section, option):
		raise Exception("config file doesn't contain {}:{}".format(section, option))
	return config[section][option]

def get_owm_token():
	section = "Tokens"
	option = "OpenWeatherMap"
	if not config.has_option(section, option):
		raise Exception("config file doesn't contain {}:{}".format(section, option))
	return config[section][option]

def get_admin_id():
    section = "Tokens"
    option = "Admin"
    if not config.has_option(section, option):
        return 0
    value = config[section][option]
    if not bool(value):
        return 0
    return value