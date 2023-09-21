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

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Chat_DB("chat.db")
db.connect()
db.init_chat_tables()


openai.api_key = openai_key


def setup_handler(dp):
    dp.message_handler(Command("Start"))(cmd_start)
    dp.message_handler(Command("menu"))(cmd_menu)
    dp.message_handler(content_types=["web_app_data"])(user_choise)
    dp.message_handler(content_types=types.ContentType.TEXT)(query_from_user)


async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    user_info = message.from_user
    user_id, username, name, surname = (
        user_info.id,
        user_info.username,
        user_info.first_name,
        user_info.last_name,
    )
    db.create_user(user_id, username, name, surname)
    keyboard = app_web_key()
    await bot.send_message(chat_id=chat_id, text=Localization.welcome_msg)
    await bot.send_message(
        chat_id=chat_id, text="Select the chatacter 👏", reply_markup=keyboard
    )
    await message.delete()


async def query_from_user(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text_of_query = message.text
    db.users_msg(user_id, text_of_query)
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
    await bot.send_message(chat_id=chat_id, text=answer_to_query)
    db.answer_msg(user_id, answer_to_query)


async def cmd_menu(message: types.Message):
    chat_id = message.chat.id
    keyboard = app_web_key()
    await bot.send_message(chat_id=chat_id, text=Localization.menu_msg)
    await bot.send_message(
        chat_id=chat_id, text="Select the chatacter 👏", reply_markup=keyboard
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
    user_info = message.from_user
    user_id, name, surname = (
        user_info.id,
        user_info.first_name,
        user_info.last_name,
    )
    chat_id = message.chat.id
    message_id = message.message_id - 1
    await message.delete()
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    user_choise = message.web_app_data.data
    db.selection_record(user_id, user_choise)
    if user_choise == "mario":
        text_of_query = f"Your name is Mario from the legendary Nintendo game, briefly greet the user named {name} {surname}, tell us about yourself and say you're willing to answer any questions you may have"
    elif user_choise == "albert":
        text_of_query = f"Your name is Albert Einstein - famous physicist - scientist, briefly greet the username {name} {surname}, tell us about yourself and say you are ready to answer any questions you may have"
    query = [
        {"role": "assistant", "content": text_of_query},
    ]
    query_to_ai = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=query)
    answer_to_query = query_to_ai["choices"][0]["message"]["content"]
    await bot.send_message(chat_id=chat_id, text=answer_to_query)
    db.answer_msg(user_id, answer_to_query)


setup_handler(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
