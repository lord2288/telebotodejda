import uuid

from yookassa import Configuration, Payment

Configuration.account_id = <Идентификатор магазина>
Configuration.secret_key = <Секретный ключ>

payment = Payment.create({
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    "description": "Заказ №1"
}, uuid.uuid4())
