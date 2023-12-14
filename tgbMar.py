from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from joblib import load
from random import choice
import tensorflow as tf
import numpy as np

BOT_TOKEN = '6487256586:AAHd1dnxlv62Y9zsM9qR7CUG9G2_QrBX_WU'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
phrases_for_users = ['What about this game', 'Try playing this', 'I think you should play this']

loaded_model = tf.keras.models.load_model("model")

tfidf_vectorizer = load('tfidf_vectorizer.bin')

label_encoder = load('label_encoder.bin')


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nЯ бот, помогающий подобрать игры по описанию!\n Введите описание игры на Английском\n\nHello!\nIm a bot that helps you find games by description!\nEnter a game description in English')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напишите мне описание игры и я постараюсь подобрать что-нибудь по вашим предпочтениям.\nЧем больше описания и подробностей вы напишите, тем лучше мы сможем подобрать вам игру!\n\nWrite me a description of the game and I will try to find something according to your preferences.\nThe more description and details you write, the better we can choose a game for you!')


@dp.message()
async def send_back(message: Message):
    input_text = message.text
    print(input_text)
    user_input_vect = tfidf_vectorizer.transform([input_text])
    predictions = loaded_model.predict(user_input_vect.toarray())
    predicted_labels = int(label_encoder.inverse_transform(
        [np.argmax(predictions)])[0])
    await message.answer(text=f'{choice(phrases_for_users)}:\nhttps://store.steampowered.com/app/{predicted_labels}')


if __name__ == '__main__':
    dp.run_polling(bot)
