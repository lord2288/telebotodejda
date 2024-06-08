import uuid
import yookassa
from app.key import yoo_kassa_key, yoo_kassa_id
from yookassa import Payment
from app.baza import reg

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
        "metadata": {
            "chat_id": chat_id
        },
        "description": "Заказ №1"
    }, id_key)
    reg()
    return payment.confirmation.confirmation_url, payment.id

def chek(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return 1
    elif payment.status == 'pending':
        return 0