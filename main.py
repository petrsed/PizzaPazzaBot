import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import *
from services.log import logging_message
from services.bdWrapper import *
from messages import *


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def send_main_keyboard(chat_id, text=MAIN_MENU_MESSAGE):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(MENU_BUTTON)
    keyboard.add(BOOKING_BUTTON, CALL_BUTTON)
    await bot.send_message(chat_id, text, reply_markup=keyboard)

async def send_admin_keyboard(chat_id, msg_id=None):
    if chat_id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Параметры", callback_data=f"admin_parameters"))
        if msg_id is None:
            await bot.send_message(chat_id, "Админ-панель:", reply_markup=markup)
        else:
            await bot.edit_message_text("Админ-панель:", chat_id, msg_id, reply_markup=markup)

@dp.callback_query_handler()
async def query_show_list(call: types.CallbackQuery, state: FSMContext):
    logging_message(call.from_user.id, call.from_user.username, call.data)
    chat_id, username, data = call.from_user.id, call.from_user.username, call.data

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if chat_id in ADMIN_IDS:
        await send_admin_keyboard(chat_id)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if not check_user_presence(chat_id):
        create_user(chat_id, username)


@dp.message_handler()
async def echo(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
