import telebot
from telebot import types
import os
import base64
import requests
import json
import time

key = '6751306928:AAFjUwlLjeMQWqBkauV1NbbXvvTnJRo4fGg'
bot = telebot.TeleBot(key)

def generate_image_from_text(prompt):
    url = 'https://api-key.fusionbrain.ai/'
    api_key = 'C620606DC592BF60C4462E27F5309E12'
    secret_key = '40D31C36DFDBD37DD3C385A7B5C143B4'
    auth_headers = {
        'X-Key': f'Key {api_key}',
        'X-Secret': f'Secret {secret_key}',
    }

    # Получаем ID модели
    response = requests.get(f"{url}key/api/v1/models", headers=auth_headers)
    response.raise_for_status()
    model_id = response.json()[0]['id']

    # Запрос на генерацию изображения
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": prompt}
    }
    data = {
        'model_id': (None, model_id),
        'params': (None, json.dumps(params), 'application/json')
    }
    response = requests.post(f"{url}key/api/v1/text2image/run", headers=auth_headers, files=data)
    response.raise_for_status()
    uuid = response.json()['uuid']

    # Проверка статуса генерации
    for _ in range(10):
        response = requests.get(f"{url}key/api/v1/text2image/status/{uuid}", headers=auth_headers)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'DONE':
            images = data['images']
            image_data = base64.b64decode(images[0])
            filename = f"generated_image.jpg"
            try:
                with open(filename, "wb") as file:
                    file.write(image_data)
                print(f"Изображение успешно сохранено как {filename}")
                return
            except Exception as e:
                print(f"Не удалось сохранить изображение: {e}")
                return
        time.sleep(10)
    print("Не удалось сгенерировать изображение.")

def pre0(message):
    global zapros
    zapros = ''

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Мужская')
    item2 = types.KeyboardButton('Женская')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Выберите пол.'.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, pre1)

def pre1(message):
    global zapros
    if message.text == 'Мужская':
        zapros += f'белый фон. на фоне мужчина в {message.text} одежде, '
    elif message.text == 'Женская':
        zapros += f'белый фон. на фоне женщина в {message.text} одежде, '
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
    markup = types.ReplyKeyboardRemove()
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
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Подождите немного', reply_markup=markup)
    generate_image_from_text(zapros)
    send_picture(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('перегенерировать')
    item2 = types.KeyboardButton('задать вид заново')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Выберите действие.'.format(message.from_user), reply_markup=markup)

def pre7(message):
    global zapros
    if message.text == 'перегенерировать':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Подождите немного', reply_markup=markup)
        generate_image_from_text(zapros)
        send_picture(message)
    elif message.text == 'задать вид заново':
        zapros = ''
        bot.register_next_step_handler(message, pre0)


def send_picture(message):
    filename = "generated_image.jpg"
    with open(filename, "rb") as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['start'])
def start(message):
    global zapros
    zapros = ''
    bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Мужская')
    item2 = types.KeyboardButton('Женская')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'Выберите пол.'.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, pre1)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем информацию о фотографии
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Скачиваем фотографию
    downloaded_file = bot.download_file(file_path)

    # Отправляем обратно фотографию
    bot.send_photo(message.chat.id, downloaded_file)

bot.polling(none_stop=True)