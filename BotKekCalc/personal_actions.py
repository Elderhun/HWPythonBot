from aiogram import Bot, Dispatcher, types, executor
import logging
from calc import *
import sqlite3

import config


import sqlite3


conn = sqlite3.connect("base.db")
cursor = conn.cursor()
    
def write_ddate_base(user_name: str, user_id : int, expression : str, result : str):
    cursor.execute("INSERT INTO bbase (user_name, user_id, expression, result) VALUES (?, ?, ?, ?)", (user_name, user_id, expression, result))
    conn.commit()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["calc"])
async def calc_command(message: types.Message):
    config.POSTING = True
    await message.answer('Пришли пример')
    
@dp.message_handler()
async def message_handler(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    expression = message.text
    if config.POSTING:
        config.POSTING = False
        
        content = arithmetic_float(message.text)
        write_ddate_base(user_name, user_id, expression, content)
        await message.answer(f'{content}')    


executor.start_polling(dp, skip_updates=True)


