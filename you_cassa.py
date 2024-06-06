import uuid

import yookassa

import key

from yookassa import Payment

yookassa.Configuration.account_id = '397814'
yookassa.Configuration.secret_key = 'test_3Y9c1M5xXOArQR6rlUnSeV35zji8zjT0vqZLbdoAUYo'

def create():
    id_key = str(uuid.uuid4())

    payment = Payment.create({
        "amount": {
            "value": "1.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/FogClothingbot"
        },
        "capture": True,
        # "metadata": {
        #     "chat_id": chat_id
        # },
        "description": "Заказ №1"
    }, id_key)
    return payment.confirmation.confirmation_url, payment.id
print(create())
