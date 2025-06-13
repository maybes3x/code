import pandas as pd
df = pd.read_excel("таблица бля бота.xlsx")

import telebot
from telebot import types

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот по персонажам Данганронпа 2.")
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Помощь', callback_data='Помощь'),
        types.InlineKeyboardButton('Инфо', callback_data='Инфо'),
        types.InlineKeyboardButton('Персонажи', callback_data='Персонажи')
    )
    bot.send_message(message.chat.id, "Выберите подходящий Вам пункт:", reply_markup=markup)
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Просто выбери персонажа из списка, и я покажу его фото и расскажу о нём!")
    bot.reply_to(message)

@bot.message_handler(commands=['info'])
def send_help(message):
    bot.send_message(message.chat.id, "Бот предоставляет изображение персонажа и информацию о нём")
    bot.reply_to(message)

@bot.callback_query_handler(func=lambda call:call.data in ['Инфо'])
def pers(call):
    back = call.data
    bot.send_message(call.message.chat.id, f"{back}: Бот предоставляет изображение персонажа и информацию о нём")

@bot.callback_query_handler(func=lambda call:call.data in ['Помощь'])
def pers(call):
    back = call.data
    bot.send_message(call.message.chat.id, f"{back}: Вы выбираете нужного Вам персонажа и смотрите информацию о нём")

@bot.callback_query_handler(func=lambda call:call.data in ['Персонажи'])
def pers(call):
    global df
    message=call.message
    lst = []
    for i in range(len(df)):
        lst.append([types.InlineKeyboardButton(f'{df["имя"].values[i]}', callback_data=f'{df["имя"].values[i]}')])
    markup = types.InlineKeyboardMarkup(lst, row_width=3)
    bot.send_message(message.chat.id, "Список всех персонажей:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def send(call):
    photo = df[df["имя"] == call.data]["фото"].values[0]
    print (photo)
    text = df[df["имя"].isin([call.data])]["инфо"].values[0]
    bot.send_photo(call.message.chat.id, photo)
    bot.send_message(call.message.chat.id, text)

bot.infinity_polling()