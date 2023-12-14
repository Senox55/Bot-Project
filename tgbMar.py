from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from keras.models import save_model, load_model
from joblib import dump, load
import tensorflow as tf
import numpy as np
import pandas as pd

BOT_TOKEN = '6487256586:AAHd1dnxlv62Y9zsM9qR7CUG9G2_QrBX_WU'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

loaded_model = tf.keras.models.load_model("model")

tfidf_vectorizer = load('tfidf_vectorizer.bin')

label_encoder = load('label_encoder.bin')


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nЯ бот, помогающий подобрать игры по описанию!\nНажмите /research и введите описание игры')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напишите мне описание игры и я постараюсь подобрать что-нибудь по вашим предпочтениям.\nЧем больше описания и подробностей вы напишите, тем лучше мы сможем подобрать вам игру!')


@dp.message()
async def send_back(message: Message):
    input_text = message.text
    print(input_text)
    user_input_vect = tfidf_vectorizer.transform([input_text])
    predictions = loaded_model.predict(user_input_vect.toarray())
    predicted_labels = int(label_encoder.inverse_transform(
        [np.argmax(predictions)])[0])
    print(predicted_labels)
    await message.answer(text=f'https://store.steampowered.com/app/{predicted_labels}')


if __name__ == '__main__':
    dp.run_polling(bot)
