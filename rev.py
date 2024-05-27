import telebot
from telebot import types
import base64
import requests
import json
import time
import sqlite3 as sq
import datetime

bot = telebot.TeleBot('6751306928:AAFjUwlLjeMQWqBkauV1NbbXvvTnJRo4fGg')

zapros = ''
available_clothing_items = {}
gender = ''

def proverka(message):
    db = sq.connect('olat.db')
    c = db.cursor()

    # Создание таблицы, если её нет
    c.execute('''CREATE TABLE IF NOT EXISTS my_table (
    id TEXT,
    date_start TEXT,
    date_end TEXT
    )
    ''')
    user = message.chat.id
    print(type(user))

    c.execute("SELECT COUNT(*) FROM my_table WHERE id=?", (user, ))
    count = c.fetchone()[0]
    # Если значения нет в базе данных, добавляем его
    if count == 0:
        return 0
    else:
        return 1

def reg(message):
    print('reg')
    db = sq.connect('olat.db')
    if message.text == 'купить подписку':
        c = db.cursor()

        # Создание таблицы, если её нет
        c.execute('''CREATE TABLE IF NOT EXISTS my_table (
        id TEXT,
        date_start TEXT,
        date_end TEXT,
        mail TEXT
        )
        ''')

        user = message.chat.id
        a = datetime.date.today()
        if a.month == 12:
            a_next = a.replace(year=a.year + 1, month=1)
        else:
            a_next = a.replace(month=a.month + 1)
            c.execute("INSERT INTO my_table (id, date_start, date_end) VALUES (?, ?, ?)",(user, a.isoformat(), a_next.isoformat()))
            db.commit()
            db.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        styles = ["Начать генерация","Информация о подипске", "Tex.поддежка" ]
        for style in styles:
            markup.add(types.KeyboardButton(style))
        bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=markup)
        bot.register_next_step_handler(message, start)

def skolko(id):
    print('skolko')
    user = id
    db = sq.connect('olat.db')
    c = db.cursor()
    c.execute("SELECT date_start, date_end FROM my_table WHERE id=?", (user,))
    result = c.fetchone()
    date_start = datetime.datetime.strptime(result[0], '%Y-%m-%d').date()
    date_end = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
    print(date_start, date_end)
    remaining_days = (date_end - date_start)
    db.commit()
    db.close()
    return f'Осталось дней: {remaining_days.days}'

def generate_image_from_text(prompt):
    try:
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
    except Exception as e:
        print(f"Ошибка при генерации изображения: {e}")
        return None

def send_picture(message, filename):
    with open(filename, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

def handle_error(message, error_text, handler):
    bot.send_message(message.chat.id, f"Произошла ошибка: {error_text}. Пожалуйста, попробуйте снова.")
    handler(message)

def start(message):
    print('start')
    print(message.text)
    if message.text == "Начать генерация":
        bot.register_next_step_handler(message, pre0)
    elif message.text == "Информация о подипске":
        bot.send_message(message.chat.id, skolko(message.chat.id))
        bot.register_next_step_handler(message, start)
    elif message.text == "Tex.поддежка":
        bot.send_message(message.chat.id, 'здесь mail человека')
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'неизвестная команда')
        bot.register_next_step_handler(message, start)

def pre0(message):
    global zapros, available_clothing_items, gender
    zapros = ''
    gender = ''
    available_clothing_items = {
        'Верхняя одежда': ['Куртка', 'Плащ', 'Жилетка', 'Ветровка', 'Поло', 'Свитер', 'Блузка', 'Рубашка', 'Свитшот', 'Водолазка', 'Топ'],
        'Нижняя одежда': ['Шорты', 'Брюки', 'Юбка', 'Джинсы'],
        'Обувь': ['Кроссовки', 'Туфли', 'Лоферы', 'Сапоги', 'Ботинки']
    }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Мужская'), types.KeyboardButton('Женская'))
    bot.send_message(message.chat.id, 'Выберите пол на кого хотите сгенерировать одежду.', reply_markup=markup)
    bot.register_next_step_handler(message, pre1)

def pre1(message):
    print(1)
    global zapros, gender
    try:
        if message.text in ['Мужская', 'Женская']:
            gender = message.text.lower()  # Store gender
            zapros += f'{gender}, в одежде, '
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            styles = ['Спортивный', 'Классический', 'Кэжуал', 'Хиппи', 'Гламур', 'Романтический']
            for style in styles:
                markup.add(types.KeyboardButton(style))
            bot.send_message(message.chat.id, 'Выберите стиль.', reply_markup=markup)
            bot.register_next_step_handler(message, pre2)
        else:
            raise ValueError("Неверный выбор пола.")
    except Exception as e:
        handle_error(message, e, pre0)

def pre2(message):
    print(2)
    global zapros
    try:
        if len(zapros) == 19:
            zapros += f'в {message.text} стиле, '
            print(zapros)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            categories = ['Верхняя одежда', 'Нижняя одежда', 'Обувь']
            for category in categories:
                if available_clothing_items[category]:  # Only add categories that have available items
                    markup.add(types.KeyboardButton(category))
            bot.send_message(message.chat.id, 'Выберите категорию одежды.', reply_markup=markup)
            bot.register_next_step_handler(message, pre3)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            categories = ['Верхняя одежда', 'Нижняя одежда', 'Обувь']
            for category in categories:
                if available_clothing_items[category]:  # Only add categories that have available items
                    markup.add(types.KeyboardButton(category))
            bot.send_message(message.chat.id, 'Выберите категорию одежды.', reply_markup=markup)
            bot.register_next_step_handler(message, pre3)
    except Exception as e:
        handle_error(message, e, pre1)

def pre3(message):
    print(3)
    global zapros, selected_category
    try:
        selected_category = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if selected_category in available_clothing_items:
            items = available_clothing_items[selected_category]
            for item in items:
                markup.add(types.KeyboardButton(item))
            zapros += f'{selected_category}: '
            bot.send_message(message.chat.id, 'Выберите конкретный элемент одежды.', reply_markup=markup)
            bot.register_next_step_handler(message, pre4)
        else:
            raise ValueError("Неверная категория одежды.")
    except Exception as e:
        handle_error(message, e, pre2)

def pre4(message):
    print(4)
    global zapros, available_clothing_items, selected_category
    try:
        selected_item = message.text
        if selected_item in available_clothing_items[selected_category]:
            zapros += f'{selected_item} '
            available_clothing_items[selected_category].remove(selected_item)  # Remove selected item from available items
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Готово'), types.KeyboardButton('Добавить еще один элемент одежды'))
            bot.send_message(message.chat.id, 'Напишите цвет одежды или добавьте еще один элемент.', reply_markup=markup)
            bot.register_next_step_handler(message, pre5)
        else:
            raise ValueError("Неверный элемент одежды.")
    except Exception as e:
        handle_error(message, e, pre3)

def pre5(message):
    print(5)
    global zapros
    try:
        if message.text == 'Готово':
            bot.send_message(message.chat.id, 'Подождите немного... Генерация изображения может составлять минуту.')
            prompt = f'Изобразите 1 человека {gender} пола в следующей одежде: {zapros}'
            print(prompt)
            filename = generate_image_from_text(prompt)
            print('gotovo')
            if filename:
                send_picture(message, filename)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row(types.KeyboardButton('Перегенерировать'), types.KeyboardButton('Задать вид заново'))
            bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=markup)
            bot.register_next_step_handler(message, pre7)
        else:
            zapros += f'а цвет {message.text}, '
            pre2(message)
    except Exception as e:
        handle_error(message, e, pre4)

def pre7(message):
    print(7)
    global zapros
    try:
        if message.text == 'Перегенерировать':
            bot.send_message(message.chat.id, 'Подождите немного... Генерация изображения может составлять минуту.')
            prompt = f'Изобразите {gender} на белом фоне в следующей одежде: {zapros}'
            filename = generate_image_from_text(prompt)
            if filename:
                send_picture(message, filename)
        elif message.text == 'Задать вид заново':
            zapros = ''
            pre0(message)
        else:
            raise ValueError("Неверный выбор действия.")
    except Exception as e:
        handle_error(message, e, pre7)

@bot.message_handler(commands=['start'])
def startt(message):
    # if proverka(message) == 1:
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     styles = ["Начать генерация", "Информация о подипске", "Tex.поддежка"]
    #     for style in styles:
    #         markup.add(types.KeyboardButton(style))
    #     bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=markup)
    #     bot.register_next_step_handler(message, start)
    # else:
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     markup.row(types.KeyboardButton('купить подписку'))
    #     bot.send_message(message.chat.id, 'вы не купили подписку', reply_markup=markup)
    #     bot.register_next_step_handler(message, reg)
    pre0(message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        bot.send_photo(message.chat.id, downloaded_file)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при обработке фотографии: {e}. Пожалуйста, попробуйте снова.")


@bot.message_handler(commands=['text'])
def text(message):
    bot.message_handler(message.chat.id, 'пока')
    bot.register_next_step_handler(message, pre0)

bot.polling(none_stop=True)
