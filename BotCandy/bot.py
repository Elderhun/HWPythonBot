from aiogram import Bot, Dispatcher, types, executor
import logging
import random
import config
import sqlite3



def proba(id):
    base = cursor.execute(f'SELECT user_id FROM Player')
    j = 0
    for i in base:
        if i[j] == id:
            return True

conn = sqlite3.connect("BotCandy/base.db")
cursor = conn.cursor()
    

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

    

def write_db(user_id: int, user_name: str, username: str):
    cursor.execute('INSERT INTO can (user_id, user_name, username) VALUES (?, ?, ?)',
                   (user_id, user_name, username))
    conn.commit()


def update_db(message, count):
    sql_update = f"UPDATE can SET candy_left = candy_left - {count} WHERE user_id == {message.from_user.id}"
    cursor.execute(sql_update)
    conn.commit()


def start(message):
    sql_update = f"UPDATE can SET candy_left = 101 WHERE user_id == {message.from_user.id}"
    cursor.execute(sql_update)
    conn.commit()


def candies(message):
    candy = f'SELECT candy_left FROM can WHERE user_id == {message.from_user.id}'
    cursor.execute(candy)
    candy_left = cursor.fetchall()
    conn.commit()
    return candy_left[0][0]


@dp.message_handler(content_types='text')
async def chat_id(message):
    p1 = message.text
    p2 = 0
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    username = message.from_user.username
    if message.text == '/start':
        start(message)
        await message.reply(f'Game is started!\n\n101 candies left\n'
                            f'\nThe first player goes! Take candies:')
        write_db(user_id=us_id, user_name=us_name, username=username)
    if p1.isdigit():
        candy = candies(message)
        if int(p1) < 1 or int(p1) > 28:
            await message.reply(f"Error!!! You can not take less than 1 and more than 28 candies\n"
                                f"\n{candy} candies left\n")
        elif int(p1) > int(candy):
            await message.reply(f"Error! You can't take more candy than you have left\n"
                                f"\n{candy} candies left\n")
        else:
            candy -= int(p1)
            update_db(message, p1)
            pn = 1
            if candy != 0:
                if candy % 29 != 0:
                    while (candy - p2) % 29 != 0:
                        p2 = random.randint(1, 28)
                    while p2 > candy and (candy - p2) % 29 != 0:
                        p2 = random.randint(1, 28)
                    while int(p2) <= 0 and (candy - p2) % 29 != 0 or int(p2) > 28 and (candy - p2) % 29 != 0:
                        p2 = random.randint(1, 28)
                        while p2 > candy and (candy - p2) % 29 != 0:
                            p2 = random.randint(1, 28)
                else:
                    while p2 > candy:
                        p2 = random.randint(1, 28)
                    while int(p2) <= 0 or int(p2) > 28:
                        p2 = random.randint(1, 28)
                        while p2 > candy:
                            p2 = random.randint(1, 28)
                await message.reply(f"\n{candy} candies left\n"
                                    f"\nBot take {p2} candies")
                candy -= p2
                update_db(message, p2)
                pn = 2
                if candy != 0:
                    await message.reply(f"\n{candy} candies left\n"
                                        f"\nThe first player goes! Take candies:")
                else:
                    await message.reply(f"\n{candy} candies left\n")
                    if pn == 1:
                        await message.reply('🎉| First player wins! Gratz!!! |🙌\n'
)
                    else:
                        await message.reply('🎉| Bot wins! Gratz!!! |🙌\n'
)
            else:
                await message.reply(f"\n{candy} candies left\n")
                if pn == 1:
                    await message.reply('🎉| First player wins! Gratz!!! |🙌\n'
)
                else:
                    await message.reply('🎉| Bot wins! Gratz!!! |🙌'
                                        )
    else:
        write_db(user_id=us_id, user_name=us_name, username=username)


executor.start_polling(dp, skip_updates=True)