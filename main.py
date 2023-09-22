from bot_setup import bot
from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import openai
from config import openai_key
from localization import Localization
from aiogram.types.web_app_info import WebAppInfo
from db.chat_db import Chat_DB
from wrappers.msg_data import MsgData

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Chat_DB("chat.db")
db.connect()
db.init_chat_tables()


openai.api_key = openai_key


def setup_handler(dp):
    dp.message_handler(Command("start"))(cmd_start)
    dp.message_handler(Command("menu"))(cmd_menu)
    dp.message_handler(content_types=["web_app_data"])(user_choise)
    dp.message_handler(content_types=types.ContentType.TEXT)(query_from_user)


async def cmd_start(message: types.Message):
    info = MsgData(message)
    db.create_user(info.user_id, info.username, info.name, info.surname)
    keyboard = app_web_key()
    await bot.send_message(chat_id=info.chat_id, text=Localization.welcome_msg)
    await bot.send_message(
        chat_id=info.chat_id, text="Select the chatacter 👏", reply_markup=keyboard
    )
    await message.delete()


async def query_from_user(message: types.Message):
    info = MsgData(message)
    db.users_msg(info.user_id, info.text)
    if text_of_query.lower == "quit" or text_of_query.lower == "/quit":
        text_of_query = "The user doesn't want to continue the dialog, you have to end it and say goodbye to them"
        query = [
            {"role": "assistant", "content": text_of_query},
        ]
    query = [
        {"role": "user", "content": text_of_query},
    ]
    query_to_ai = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=query)
    answer_to_query = query_to_ai["choices"][0]["message"]["content"]
    await bot.send_message(info.chat_id, text=answer_to_query)
    db.answer_msg(info.user_id, answer_to_query)


async def cmd_menu(message: types.Message):
    info = MsgData(message)
    keyboard = app_web_key()
    await bot.send_message(chat_id=info.chat_id, text=Localization.menu_msg)
    await bot.send_message(
        chat_id=info.chat_id, text="Select the chatacter 👏", reply_markup=keyboard
    )
    db.fetch_all_data()
    await message.delete()


def app_web_key():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton(
        "select a character",
        web_app=WebAppInfo(url="https://volynkinss.github.io/page_for_bot"),
    )
    keyboard.add(button)
    return keyboard


async def user_choise(message: types.Message):
    info = MsgData(message)
    await bot.delete_message(chat_id=info.chat_id, message_id=info.message_id)
    db.selection_record(info.chat_id, info.user_choise)
    if info.user_choise == "mario":
        text_of_query = f"Your name is Mario from the legendary Nintendo game, briefly greet the user named {info.name} {info.surname}, tell us about yourself and say you're willing to answer any questions you may have"
    elif info.user_choise == "albert":
        text_of_query = f"Your name is Albert Einstein - famous physicist - scientist, briefly greet the username {info.name} {info.surname}, tell us about yourself and say you are ready to answer any questions you may have"
    query = [
        {"role": "assistant", "content": text_of_query},
    ]
    query_to_ai = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=query)
    answer_to_query = query_to_ai["choices"][0]["message"]["content"]
    await bot.send_message(chat_id=info.chat_id, text=answer_to_query)
    db.answer_msg(info.user_id, answer_to_query)


setup_handler(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
