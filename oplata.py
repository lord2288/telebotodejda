import sqlite3 as sq
import datetime
import telebot

db = sq.connect('olat.db')
c = db.cursor()

# Создание таблицы, если её нет
c.execute('''CREATE TABLE IF NOT EXISTS my_table (
id TEXT,
date_start TEXT,
date_end TEXT
)
''')

def proverka(idd):
    user = idd

    c.execute("SELECT COUNT(*) FROM my_table WHERE id=?", (user, ))
    count = c.fetchone()[0]
    # Если значения нет в базе данных, добавляем его
    if count == 0:
        return 0
    else:
        return 1
def reg(idd):
    user = idd
    a = datetime.date.today()
    if a.month == 12:
        a_next = a.replace(year=a.year + 1, month=1)
    else:
        a_next = a.replace(month=a.month + 1)
    c.execute("INSERT INTO my_table (id, date_start, date_end) VALUES (?, ?, ?)",
              (user, a.isoformat(), a_next.isoformat()))
# else:
#     c.execute("SELECT date_start, date_end FROM my_table WHERE id=?", (user,))
#         result = c.fetchone()
#         date_start = datetime.datetime.strptime(result[0], '%Y-%m-%d').date()
#         date_end = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
#         remaining_days = (date_end - datetime.date.today()).days
#         print(f'Осталось дней: {remaining_days}')
#
#     db.commit()
#     db.close()