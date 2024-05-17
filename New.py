import telebot
from telebot import types
import base64
import requests
import json
import time

bot = telebot.TeleBot('6751306928:AAFjUwlLjeMQWqBkauV1NbbXvvTnJRo4fGg')

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
                return filename
            except Exception as e:
                print(f"Не удалось сохранить изображение: {e}")
                return None
        time.sleep(10)
    return None

def send_picture(message, filename):
    with open(filename, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

def pre0(message):
    global zapros
    zapros = ''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Мужская'), types.KeyboardButton('Женская'))
    bot.send_message(message.chat.id, 'Выберите пол на кого хотите сгенерировать одежду.', reply_markup=markup)
    bot.register_next_step_handler(message, pre1)

def pre1(message):
    global zapros
    if message.text in ['Мужская', 'Женская']:
        zapros += f'белый фон. на фоне {message.text.lower()} в одежде, '
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        styles = ['Спортивный', 'Классический', 'Кэжуал', 'Хиппи', 'Гламур', 'Романтический']
        for style in styles:
            markup.add(types.KeyboardButton(style))
        bot.send_message(message.chat.id, 'Выберите стиль.', reply_markup=markup)
        bot.register_next_step_handler(message, pre2)
    else:
        pre0(message)

def pre2(message):
    global zapros
    zapros += f'в {message.text} Стиле, '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ['Верхняя одежда-пальто', 'Верхняя одежда-футболка', 'Нижняя одежда-шорты']
    for category in categories:
        markup.add(types.KeyboardButton(category))
    bot.send_message(message.chat.id, 'Выберите категорию одежды.', reply_markup=markup)
    bot.register_next_step_handler(message, pre3)

def pre3(message):
    global zapros
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Верхняя одежда-пальто':
        items = ['Куртка', 'Плащ', 'Жилетка', 'Ветровка']
    elif message.text == 'Верхняя одежда-футболка':
        items = ['Поло', 'Свитер', 'Блузка', 'Рубашка', 'Свитшот', 'Водолазка', 'Топ']
    elif message.text == 'Нижняя одежда-шорты':
        items = ['Шорты', 'Брюки', 'Юбка', 'Джинсы']
    else:
        pre2(message)
        return
    for item in items:
        markup.add(types.KeyboardButton(item))
    zapros += f'{message.text}, '
    bot.send_message(message.chat.id, 'Выберите конкретный элемент одежды.', reply_markup=markup)
    bot.register_next_step_handler(message, pre4)

def pre4(message):
    global zapros
    zapros += f'{message.text}, '
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Напишите цвет одежды.', reply_markup=markup)
    bot.register_next_step_handler(message, pre5)

def pre5(message):
    global zapros
    zapros += f'Цвет {message.text}, '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    footwear = ['Кроссовки', 'Туфли', 'Лоферы', 'Сапоги', 'Ботинки']
    for item in footwear:
        markup.add(types.KeyboardButton(item))
    bot.send_message(message.chat.id, 'Выберите обувь.', reply_markup=markup)
    bot.register_next_step_handler(message, pre6)

def pre6(message):
    global zapros
    zapros += f'На ногах {message.text}.'
    bot.send_message(message.chat.id, """Подождите немного...
Генерация изображения может составлять минуту """)
    filename = generate_image_from_text(zapros)
    if filename:
        send_picture(message, filename)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Перегенерировать'), types.KeyboardButton('Задать вид заново'))
    bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=markup)
    bot.register_next_step_handler(message, pre7)

def pre7(message):
    global zapros
    if message.text == 'Перегенерировать':
        bot.send_message(message.chat.id, """Подождите немного...
Генерация изображения может составлять минуту """)

        filename = generate_image_from_text(zapros)
        if filename:
            send_picture(message, filename)
    elif message.text == 'Задать вид заново.':
        zapros = ''
        pre0(message)
    else:
        pre6(message)

@bot.message_handler(commands=['start'])
def start(message):
    pre0(message)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    bot.send_photo(message.chat.id, downloaded_file)

bot.polling(none_stop=True)
