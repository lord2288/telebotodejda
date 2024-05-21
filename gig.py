#dae3b828-0a56-4841-b784-d98e34a34be7
#YzcyZDdmZmItNWEyNC00MmNmLWFmZTQtNWMyZGEzNDQ5NmRhOmRhZTNiODI4LTBhNTYtNDg0MS1iNzg0LWQ5OGUzNGEzNGJlNw==
"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='YzcyZDdmZmItNWEyNC00MmNmLWFmZTQtNWMyZGEzNDQ5NmRhOmRhZTNiODI4LTBhNTYtNDg0MS1iNzg0LWQ5OGUzNGEzNGJlNw==', verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

while(True):
    # Ввод пользователя
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot: ", res.content)