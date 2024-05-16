import telebot
from telebot import types

key = '6751306928:AAFjUwlLjeMQWqBkauV1NbbXvvTnJRo4fGg'
bot = telebot.TeleBot(key)
def pre1(message):
    global zapros
    zapros += f'белый фон на фоне человек в {message.text} одежде, '
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
    zapros += f'в {message.text} стиле '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('верхняя одежда-польто')
    item2 = types.KeyboardButton('верхняя одежда-футболка')
    item3 = types.KeyboardButton('нижняя одежда-шорты')
    markup.row(item1, item2, item3)
    bot.send_message(message.chat.id, 'выбирете уровень одежды', reply_markup=markup)
    bot.register_next_step_handler(message, pre3)
def pre3(message):
    global zapros
    # zapros += f'в {message.text}'
    if message.text == "верхняя одежда-польто":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('куртка')
        item2 = types.KeyboardButton('плащ')
        item3 = types.KeyboardButton('жилетка')
        item4 = types.KeyboardButton('ветровка')
        markup.row(item1, item2, item3, item4)
        bot.send_message(message.chat.id, 'выбирете уровень одежды', reply_markup=markup)
    elif message.text == "верхняя одежда-футболка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('поло')
        item2 = types.KeyboardButton('свитер')
        item3 = types.KeyboardButton('блузка')
        item4 = types.KeyboardButton('рубашка')
        item5 = types.KeyboardButton('свитшот')
        item6 = types.KeyboardButton('водолазка')
        item7 = types.KeyboardButton('топ')
        markup.row(item1, item2, item3, item4, item5, item6, item7)
        bot.send_message(message.chat.id, 'выбирете уровень одежды', reply_markup=markup)
    elif message.text == 'нижняя одежда-шорты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('шорты')
        item2 = types.KeyboardButton('брюки')
        item3 = types.KeyboardButton('юбка')
        item4 = types.KeyboardButton('джинсы')
        markup.row(item1, item2, item3, item4)
        bot.send_message(message.chat.id, 'выбирете одежду', reply_markup=markup)
    bot.register_next_step_handler(message, pre4)

def pre4(message):
    global zapros
    zapros += f'в {message.text} '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row()
    bot.send_message(message.chat.id, 'напишите цвет одежды', reply_markup=markup)
    bot.register_next_step_handler(message, pre5)


def pre5(message):
    global zapros
    zapros += f'цвет этой одежды {message.text} '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('кроссовки')
    item2 = types.KeyboardButton('туфли')
    item3 = types.KeyboardButton('лоферы')
    item4 = types.KeyboardButton('сапоги')
    item5 = types.KeyboardButton('ботинки')
    markup.row(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'выбирете обувь', reply_markup=markup)
    bot.register_next_step_handler(message, pre6)

def pre6(message):
    global zapros
    zapros += f'а на ногах {message.text}'
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