from aiogram import types
from misc import dp

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("/help")
    
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):
    await message.answer("unknown command")    
    