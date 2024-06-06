import random
import asyncio
import aiohttp  # Добавлено для работы с запросами к API
from aiogram import Dispatcher, Bot, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_TOKEN
from datetime import datetime

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    inline_btn_1 = InlineKeyboardButton('Перейти на 2 клавиатуру', callback_data='to_keyboard_2')
    inline_btn_2 = InlineKeyboardButton('Отправь случайное число', callback_data='set_random_number')
    inline_btn_3 = InlineKeyboardButton('Отправь текущее время', callback_data='set_datetime')
    inline_btn_4 = InlineKeyboardButton('Отправь случайный смайлик', callback_data='send_random_emoji')
    inline_btn_5 = InlineKeyboardButton('Узнать IP-адрес', callback_data='get_ip')
    inline_kb.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)
    await message.reply('Ты на первой 1, нажми чтобы перейти на 2 клавиатуру',
                        reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'set_random_number')
async def random_number(callback_query: types.CallbackQuery):
    random_num = random.randint(1, 100)
    message = await callback_query.message.answer(f'Ваше случайное число: {random_num}')
    await asyncio.sleep(5)
    await message.delete()

@dp.callback_query_handler(lambda c: c.data == 'set_datetime')
async def set_datetime(callback_query: types.CallbackQuery):
    current_time = datetime.now().strftime("%H:%M:%S")
    message = await callback_query.message.answer(f'Текущее время: {current_time}')
    await asyncio.sleep(5)
    await message.delete()

@dp.callback_query_handler(lambda c: c.data == 'send_random_emoji')
async def send_random_emoji(callback_query: types.CallbackQuery):
    emojis = ['😊', '😂', '🥰', '😎', '😜', '🤔', '😇']
    random_emoji = random.choice(emojis)
    message = await callback_query.message.answer(f'Ваш случайный смайлик: {random_emoji}')
    await asyncio.sleep(5)
    await message.delete()

@dp.callback_query_handler(lambda c: c.data == 'get_ip')
async def get_ip(callback_query: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ipify.org?format=json') as resp:
            if resp.status == 200:
                data = await resp.json()
                ip_address = data['ip']
                message = await callback_query.message.answer(f'Ваш IP-адрес: {ip_address}')
                await asyncio.sleep(10)
                await message.delete()
            else:
                message = await callback_query.message.answer('Не удалось получить IP-адрес.')
                await asyncio.sleep(10)
                await message.delete()

@dp.callback_query_handler(lambda c: c.data == 'to_keyboard_2')
async def process_callback_keyboard2(callback_query: types.CallbackQuery):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    inline_btn_1 = InlineKeyboardButton('Назад на 1 клавиатуру', callback_data='to_keyboard_1')
    inline_btn_2 = InlineKeyboardButton('Отправь текущее время', callback_data='set_datetime')
    inline_btn_3 = InlineKeyboardButton('Отправь случайный смайлик', callback_data='send_random_emoji')
    inline_btn_4 = InlineKeyboardButton('Узнать IP-адрес', callback_data='get_ip')
    inline_kb.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4)
    await callback_query.message.edit_text('Ты на второй 2, нажми чтобы вернуться на 1 клавиатуру',
                                           reply_markup=inline_kb)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'to_keyboard_1')
async def process_callback_keyboard1(callback_query: types.CallbackQuery):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    inline_btn_1 = InlineKeyboardButton('Перейти на 2 клавиатуру', callback_data='to_keyboard_2')
    inline_btn_2 = InlineKeyboardButton('Отправь случайное число', callback_data='set_random_number')
    inline_btn_3 = InlineKeyboardButton('Отправь текущее время', callback_data='set_datetime')
    inline_btn_4 = InlineKeyboardButton('Отправь случайный смайлик', callback_data='send_random_emoji')
    inline_btn_5 = InlineKeyboardButton('Узнать IP-адрес', callback_data='get_ip')
    inline_kb.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)
    await callback_query.message.edit_text('Ты на первой 1, нажми чтобы перейти на 2 клавиатуру',
                                           reply_markup=inline_kb)
    await bot.answer_callback_query(callback_query.id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
