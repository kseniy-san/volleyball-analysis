import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Список всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Таблицы в базе данных:")
for table in tables:
    print(f"- {table[0]}")

conn.close()