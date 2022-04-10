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


@dp.message_handler(content_types=["photo"])
async def echo(message: types.Message):
    print(message.photo[-1].file_id)

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

def get_prev_next_products(product_id):
    product = get_position_by_id(product_id)
    category_products = [category[0] for category in get_category_positions(product[1])]
    product_index = category_products.index(int(product_id))
    prev_id, next_id = product_index - 1, product_index + 1
    if next_id == len(category_products):
        next_id = 0
    prev_product = get_position_by_id(category_products[prev_id])
    next_product = get_position_by_id(category_products[next_id])
    return prev_product[0], next_product[0]

async def send_menu(chat_id, text=MENU_TEXT, msg_id=None):
    categories = get_all_categories()
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.add(types.InlineKeyboardButton(category[1], callback_data=f"category_{category[0]}"))
    if msg_id is None:
        await bot.send_message(chat_id, text, reply_markup=markup)
    else:
        await bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup)

async def send_category_positions(chat_id, product_id, msg_id=None, delete_old_message=False):
    product = get_position_by_id(product_id)
    category = get_category_by_id(product[1])
    prev_product_id, next_product_id = get_prev_next_products(product_id)
    msg = PRODUCT_TEXT
    msg = msg.replace("{CATEGORY}", category[1])
    msg = msg.replace("{NAME}", product[2])
    msg = msg.replace("{DESCRIPTION}", product[3])
    msg = msg.replace("{PRICE}", str(product[5]))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(LEFT_EMOJI, callback_data=f"product_{prev_product_id}"),
               types.InlineKeyboardButton(RIGHT_EMOJI, callback_data=f"product_{next_product_id}"))
    markup.add(types.InlineKeyboardButton(RETURN_BUTTON, callback_data=f"catalog"))
    if msg_id is not None:
        if delete_old_message:
            await bot.delete_message(chat_id, msg_id)
        else:
            await bot.edit_message_media(types.InputMediaPhoto(product[4], caption=msg, parse_mode="HTML"), chat_id, msg_id, reply_markup=markup)
            return
    await bot.send_photo(chat_id, product[4], caption=msg, parse_mode="HTML", reply_markup=markup)

@dp.callback_query_handler()
async def query_show_list(call: types.CallbackQuery, state: FSMContext):
    logging_message(call.from_user.id, call.from_user.username, call.data)
    chat_id, username, data = call.from_user.id, call.from_user.username, call.data
    if "category_" in data:
        category_id = data.split("_")[1]
        positions = get_category_positions(category_id)
        await send_category_positions(chat_id, positions[0][0], call.message.message_id, delete_old_message=True)
    elif "product_" in data:
        product_id = data.split("_")[1]
        await send_category_positions(chat_id, product_id, call.message.message_id)
    elif data == "catalog":
        await bot.delete_message(chat_id, call.message.message_id)
        await send_menu(chat_id)

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
    await send_main_keyboard(chat_id, WELCOME_MESSAGE)


@dp.message_handler()
async def echo(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if text == MENU_BUTTON:
        await send_menu(chat_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
