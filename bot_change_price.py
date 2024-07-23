import json
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

with open('data.json', 'r') as f:
    manage = json.load(f)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Roman")],
        [types.KeyboardButton(text="Dmitriy")],
        [types.KeyboardButton(text="Andrey_P")],
        [types.KeyboardButton(text="Sergey")],
        [types.KeyboardButton(text="Andrey_K")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    # await message.answer("Привет!\nСюда Вы будете получать сообщения:\n1) Если не правильно заполнили КЦ в карточке товара.\n2) Если вы хотите получить файл с выгодными предложениями для закупки на СММ.")
    await message.answer("Выберите Ваше Имя", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in {"Roman", "Dmitriy", "Andrey_P", "Sergey", "Andrey_K"})
async def greet_user(message: types.Message):
    # Приветствие с повторением слова

    manage[message.from_user.id] = message.text
    with open('data.json', 'w') as f:
        json.dump(manage, f)
    await message.answer(f"Отлично!",
                         reply_markup=types.ReplyKeyboardRemove())
    # kb = [[types.KeyboardButton(text="Получить прайс")]]
    # await message.answer(f"Теперь Вы можете получать прайс выгодных предложений на СММ\nи уведомления", reply_markup=types.ReplyKeyboardRemove())
    # await message.answer("Для этого нужно нажать кнопку", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb))


@dp.message_handler(text='Получить прайс')
async def get_price(message: types.Message):
    manager = manage[str(message.from_user.id)]
    await message.answer_document(open(fr'./offers_price/{manager}.xlsx', 'rb'))


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)