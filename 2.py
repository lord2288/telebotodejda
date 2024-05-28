import logging
import telebot
from telebot import types
import base64
import requests
import json
import time
import sqlite3 as sq
import datetime
import key

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота
bot = telebot.TeleBot(key.telebot_api)

# Инициализация базы данных
def init_db():
    with sq.connect('olat.db') as db:
        db.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
            id TEXT PRIMARY KEY,
            date_start TEXT,
            date_end TEXT,
            mail TEXT
        )''')

# Проверка подписки
def is_subscribed(user_id):
    with sq.connect('olat.db') as db:
        result = db.execute("SELECT COUNT(*) FROM subscriptions WHERE id=?", (user_id,)).fetchone()
        return result[0] > 0

# Регистрация подписки
def register_subscription(user_id):
    with sq.connect('olat.db') as db:
        date_start = datetime.date.today()
        date_end = (date_start.replace(month=date_start.month + 1) if date_start.month != 12
                    else date_start.replace(year=date_start.year + 1, month=1))
        db.execute("INSERT INTO subscriptions (id, date_start, date_end, mail) VALUES (?, ?, ?, ?)",
                   (user_id, date_start.isoformat(), date_end.isoformat(), None))

# Количество дней до окончания подписки
def days_left(user_id):
    with sq.connect('olat.db') as db:
        result = db.execute("SELECT date_end FROM subscriptions WHERE id=?", (user_id,)).fetchone()
        date_end = datetime.datetime.strptime(result[0], '%Y-%m-%d').date()
        return (date_end - datetime.date.today()).days

# Генерация изображения по тексту
def generate_image_from_text(prompt):
    try:
        url = 'https://api-key.fusionbrain.ai/'
        api_key = 'C620606DC592BF60C4462E27F5309E12'
        secret_key = '40D31C36DFDBD37DD3C385A7B5C143B4'
        headers = {'X-Key': f'Key {api_key}', 'X-Secret': f'Secret {secret_key}'}

        response = requests.get(f"{url}key/api/v1/models", headers=headers)
        response.raise_for_status()
        model_id = response.json()[0]['id']

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
        response = requests.post(f"{url}key/api/v1/text2image/run", headers=headers, files=data)
        response.raise_for_status()
        uuid = response.json()['uuid']

        for _ in range(10):
            response = requests.get(f"{url}key/api/v1/text2image/status/{uuid}", headers=headers)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'DONE':
                image_data = base64.b64decode(data['images'][0])
                filename = "generated_image.jpg"
                with open(filename, "wb") as file:
                    file.write(image_data)
                return filename
            time.sleep(10)
        return None
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return None

# Отправка изображения
def send_image(chat_id, filename):
    with open(filename, "rb") as photo:
        bot.send_photo(chat_id, photo)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # user_id = message.chat.id
    # if is_subscribed(user_id):
    #     show_main_menu(message)
    # else:
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     markup.row(types.KeyboardButton('купить подписку'))
    #     bot.send_message(user_id, 'вы не купили подписку', reply_markup=markup)
    #     bot.register_next_step_handler(message, handle_subscription)
    bot.register_next_step_handler(message, show_main_menu)

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Извините за предоставленные неудобства, начните пожалуйста заново.')
    show_main_menu(message)

# Обработка подписки
def handle_subscription(message):
    if message.text == 'купить подписку':
        register_subscription(message.chat.id)
        show_main_menu(message)

# Показ главного меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    options = ["Начать генерация", "Tex.поддержка"]
    markup.add(*[types.KeyboardButton(option) for option in options])
    bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=markup)
    bot.register_next_step_handler(message, handle_main_menu)

# Обработка главного меню
def handle_main_menu(message):
    if message.text == "Начать генерация":
        start_generation(message)
    elif message.text == "Информация о подписке":
        bot.send_message(message.chat.id, f'Осталось дней: {days_left(message.chat.id)}')
        show_main_menu(message)
    elif message.text == "Tex.поддержка":
        bot.send_message(message.chat.id, 'здесь mail человека')
        show_main_menu(message)
    else:
        bot.send_message(message.chat.id, 'неизвестная команда')
        show_main_menu(message)

# Начало генерации
def start_generation(message):
    global request_data
    request_data = {'gender': '', 'style': '', 'clothing': []}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Мужская'), types.KeyboardButton('Женская'))
    bot.send_message(message.chat.id, 'Выберите пол.', reply_markup=markup)
    bot.register_next_step_handler(message, choose_gender)

# Выбор пола
def choose_gender(message):
    if message.text in ['Мужская', 'Женская']:
        request_data['gender'] = message.text.lower()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        styles = ['Спортивный', 'Классический', 'Кэжуал', 'Хиппи', 'Гламур', 'Романтический']
        markup.add(*[types.KeyboardButton(style) for style in styles])
        bot.send_message(message.chat.id, 'Выберите стиль.', reply_markup=markup)
        bot.register_next_step_handler(message, choose_style)
    else:
        bot.send_message(message.chat.id, 'Неверный выбор пола.')
        start_generation(message)

# Выбор стиля
def choose_style(message):
    request_data['style'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ['Верхняя одежда', 'Нижняя одежда', 'Обувь']
    markup.add(*[types.KeyboardButton(category) for category in categories])
    bot.send_message(message.chat.id, 'Выберите категорию одежды.', reply_markup=markup)
    bot.register_next_step_handler(message, choose_category)

# Выбор категории
def choose_category(message):
    request_data['category'] = message.text
    items = {
        'Верхняя одежда': ['Куртка', 'Плащ', 'Жилетка', 'Ветровка', 'Поло', 'Свитер', 'Блузка', 'Рубашка', 'Свитшот',
                           'Водолазка', 'Топ'],
        'Нижняя одежда': ['Шорты', 'Брюки', 'Юбка', 'Джинсы'],
        'Обувь': ['Кроссовки', 'Туфли', 'Лоферы', 'Сапоги', 'Ботинки']
    }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(item) for item in items.get(message.text, [])])
    bot.send_message(message.chat.id, 'Выберите элемент одежды или нажмите "Готово" для завершения.',
                     reply_markup=markup)
    bot.register_next_step_handler(message, choose_item)


def choose_item(message):
    if message.text == 'Готово':
        finalize_selection(message)
    else:
        request_data['clothing'].append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('Готово'), types.KeyboardButton('Добавить еще один элемент одежды'))
        bot.send_message(message.chat.id, 'Напишите цвет одежды или добавьте еще один элемент.', reply_markup=markup)
        bot.register_next_step_handler(message, finalize_or_add)


def finalize_or_add(message):
    if message.text == 'Готово':
        finalize_selection(message)
    elif message.text == 'Добавить еще один элемент одежды':
        choose_style(message)
    # else:
    #     bot.send_message(message.chat.id, 'Неверный выбор.')
    #     finalize_or_add(message)

# Завершение выбора и генерация изображения
def finalize_selection(message):
    generate_and_send_image(message)

# Генерация и отправка изображения
def generate_and_send_image(message):
    bot.send_message(message.chat.id, 'Подождите, идет генерация изображения...')
    prompt = f"Изобразите {request_data['gender']} в стиле {request_data['style']} с одеждой: {', '.join(request_data['clothing'])}"
    filename = generate_image_from_text(prompt)
    if filename:
        send_image(message.chat.id, filename)
    show_main_menu(message)

# Основная функция
def main():
    init_db()
    bot.polling(none_stop=True, interval=2)

# Запуск бота
if __name__ == "__main__":
    while True:
        try:
            logging.info("Bot running..")
            main()
        except telebot.apihelper.ApiException as e:
            logging.error(e)
            time.sleep(15)
            logging.info("Running again!")
