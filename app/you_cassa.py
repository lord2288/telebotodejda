import uuid
import yookassa
from app.key import yoo_kassa_key, yoo_kassa_id
from yookassa import Payment
from app.baza import reg
import sqlite3 as sq

yookassa.Configuration.account_id = yoo_kassa_id
yookassa.Configuration.secret_key = yoo_kassa_key

def create(chat_id):
    id_key = str(uuid.uuid4())

    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/FogClothingbot"
        },
        "capture": True,
        "description": "Заказ №1"
    }, id_key)
    reg(chat_id, payment.id)
    return payment.confirmation.confirmation_url

def chek(user_id):
    db = sq.connect('olat.db')
    c = db.cursor()

    c.execute("SELECT payment_id FROM your_table WHERE user_id=?", (user_id,))

    # Извлечение результата
    result = c.fetchone()

    payment = yookassa.Payment.find_one(result)
    if payment.status == 'succeeded':
        return 1
    elif payment.status == 'pending':
        return 0