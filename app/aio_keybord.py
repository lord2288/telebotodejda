from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='начать генерацию')],
                                     [KeyboardButton(text='проверить подписку'),
                                      KeyboardButton(text='Tex.поддежка')]],
                           resize_keyboard=True)
gender = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='мужчина'),
    KeyboardButton(text='женщина')
]],
    resize_keyboard=True)

style = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Спортивный'),
    KeyboardButton(text='Классический')],
[
    KeyboardButton(text='Кэжуал'),
    KeyboardButton(text='Хиппи')],
[
    KeyboardButton(text='Гламур'),
    KeyboardButton(text='Романтический')]],
    resize_keyboard=True)

outerwear = ReplyKeyboardMarkup(keyboard=[
[
    KeyboardButton(text='Куртка'),
    KeyboardButton(text='Плащ'),
    KeyboardButton(text='Жилетка')
],
[
    KeyboardButton(text='Ветровка'),
    KeyboardButton(text='Поло'),
    KeyboardButton(text='Свитер')
],
[
    KeyboardButton(text='Блузка'),
    KeyboardButton(text='Рубашка'),
    KeyboardButton(text='Свитшот')
],
[
    KeyboardButton(text='Водолазка'),
    KeyboardButton(text='Топ')
]
], resize_keyboard=True)

underwear = ReplyKeyboardMarkup(keyboard=[
[
    KeyboardButton(text='Шорты'),
    KeyboardButton(text='Брюки')
],
[
    KeyboardButton(text='Юбка'),
    KeyboardButton(text='Джинсы')
],
], resize_keyboard=True)

shoes = ReplyKeyboardMarkup(keyboard=[
[
    KeyboardButton(text='Кроссовки'),
    KeyboardButton(text='Туфли')
],
[
    KeyboardButton(text='Лоферы'),
    KeyboardButton(text='Сапоги')
],
[
    KeyboardButton(text='Ботинки'),
]
], resize_keyboard=True)

gotovo = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Перегенерировать'),
    KeyboardButton(text='задать вид заново')
],
[
    KeyboardButton(text='Вернутся в главное меню'),
]
],
    resize_keyboard=True)

