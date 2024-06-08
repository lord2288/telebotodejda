import sqlite3 as sq
import datetime

db = sq.connect('oplat.db')
c = db.cursor()

# Создание таблицы, если её нет
c.execute('''CREATE TABLE IF NOT EXISTS my_table (
id TEXT,
date_start TEXT,
date_end TEXT,
payment_id TEXT
)
''')

def proverka(idd):
    db = sq.connect('olat.db')
    c = db.cursor()
    user = idd

    c.execute("SELECT COUNT(*) FROM my_table WHERE id=?", (user, ))
    count = c.fetchone()[0]
    # Если значения нет в базе данных, добавляем его
    if count == 0:
        return 0
    else:
        return 1

def reg(idd, payment_id):
    db = sq.connect('olat.db')
    c = db.cursor()
    user = idd
    a = datetime.date.today()
    if a.month == 12:
        a_next = a.replace(year=a.year + 1, month=1)
    else:
        a_next = a.replace(month=a.month + 1)
    c.execute("INSERT INTO my_table (id, date_start, date_end, payment_id) VALUES (?, ?, ?, ?)",
              (user, a.isoformat(), a_next.isoformat(), payment_id))
    db.commit()
    db.close()
def check(id):
    db = sq.connect('olat.db')
    c = db.cursor()
    user = id
    c.execute("SELECT date_start, date_end FROM my_table WHERE id=?", (user,))
    result = c.fetchone()
    date_start = datetime.datetime.strptime(result[0], '%Y-%m-%d').date()
    date_end = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
    remaining_days = (date_end - datetime.date.today()).days
    return (f'Осталось дней: {remaining_days}')
