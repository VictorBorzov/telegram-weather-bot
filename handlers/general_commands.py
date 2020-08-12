from aiogram import types 
from misc import dp, bot
from settings import get_admin_id

admin_id = int(get_admin_id())

handled_commands = {"/weather_by_city" : "get weather forecast at city",
                    "/weather_by_gps"  : "get weather forecast at my location"}

@dp.message_handler(commands="update_hint", state="*")
async def cmd_update_hint(message: types.Message):
    if message.from_user.id == admin_id:  
        commands = []
        for handled_command, handled_command_description in handled_commands.items():
            commands.append(types.BotCommand(command=handled_command, description=handled_command_description))            
        await bot.set_my_commands(commands)
        await message.answer("Command hint udpated.")    

@dp.message_handler(commands=["help", "start"])
async def cmd_start(message: types.Message):
    msg = ""
    # tmp added for new bot ->
    commands = []
    for handled_command, handled_command_description in handled_commands.items():
        commands.append(types.BotCommand(command=handled_command, description=handled_command_description))            
    await bot.set_my_commands(commands)
    # <- tmp added for new bot
    for handled_command, handled_command_description in handled_commands.items():
        msg += handled_command + " - " + handled_command_description + "\n"
    await message.answer(msg)


@dp.message_handler(commands="my_id", state="*")
async def cmd_get_user_id(message: types.Message):
    user_id = message.from_user.id
    if user_id == admin_id:
        user_id = "{} (admin)".format(user_id)
    await message.answer(user_id)    
