import telebot
from telebot import types
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

api = "7278653717:AAGkNKVfBgRSSL5ZjSS2VgQEmXLaJTVxzME"


# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='YzcyZDdmZmItNWEyNC00MmNmLWFmZTQtNWMyZGEzNDQ5NmRhOmRhZTNiODI4LTBhNTYtNDg0MS1iNzg0LWQ5OGUzNGEzNGJlNw==', verify_ssl_certs=False)
bot = telebot.TeleBot(api)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте я gigamen. Чем я могу вам помочь")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_input = message.text
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    bot.send_message(message.chat.id, res.content)

bot.polling(none_stop=True)