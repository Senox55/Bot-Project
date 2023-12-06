from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '6487256586:AAHd1dnxlv62Y9zsM9qR7CUG9G2_QrBX_WU'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nЯ бот, помогающий подобрать игры по описанию!\nНажмите /research и введите описание игры')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напишите мне описание игры и я постараюсь подобрать что-нибудь по вашим предпочтениям.\nЧем больше описания и подробностей вы напишите, тем лучше мы сможем подобрать вам игру!')


@dp.message(Command(commands=['research']))
async def process_help_command(message: Message):
    await message.answer('Введите описание игры :')


if __name__ == '__main__':
    dp.run_polling(bot)
