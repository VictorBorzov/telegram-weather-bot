from aiogram import types 
from misc import dp, bot

@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    if message.from_user.id == 398978035:  
        commands = [types.BotCommand(command="/weather_by_city", description="search city"), 
					types.BotCommand(command="/weather_by_gps", description="share my location")]
        await bot.set_my_commands(commands)
        await message.answer("Command hint udpated.")    

