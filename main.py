import telebot
from telebot import types

key = '6751306928:AAFjUwlLjeMQWqBkauV1NbbXvvTnJRo4fGg'
bot = telebot.TeleBot(key)
def pre1(message):
    global zapros
    zapros += f'{message.text}/'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('спортивный')
    item2 = types.KeyboardButton('клачический')
    item3 = types.KeyboardButton('кэжуал')

    item5 = types.KeyboardButton('хиппи')
    item6 = types.KeyboardButton('гламур')
    item7 = types.KeyboardButton('романтический')
    markup.row(item1, item2, item3)
    markup.row(item5, item6, item7)
    bot.send_message(message.chat.id, 'выбирете стиль', reply_markup=markup)
    bot.register_next_step_handler(message, pre2)

def pre2(message):
    global zapros
    zapros += f'{message.text}/'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('верхняя одежда-польто')
    item2 = types.KeyboardButton('верхняя одежда-футболка')
    item3 = types.KeyboardButton('ижняя одежда-шорты')
    markup.row(item1, item2, item3)
    bot.send_message(message.chat.id, 'выбирете уровень одежды', reply_markup=markup)
    bot.register_next_step_handler(message, pre3)
def pre3(message):
    global zapros
    zapros += f'{message.text}/'
    if message.text == "верхняя одежда-польто":
        bot.send_message(message.chat.id, zapros)
@bot.message_handler(commands=['start'])
def start(message):
    global zapros
    zapros = ''
    bot.send_message(message.chat.id, 'Выберите пол.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Мужская')
    item2 = types.KeyboardButton('Женская')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, pre1)

bot.polling(none_stop=True)