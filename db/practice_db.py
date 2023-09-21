import sqlite3

db = sqlite3.connect("base_one.db")
cursor = db.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (name TEXT, surname TEXT, age INT)"""
)
db.commit()

name = input("Name: ")
surname = input("Surname: ")
age = input("Age: ")


if cursor.execute("SELECT name FROM users") == name:
    cursor.execute(f"INSERT INTO users VALUES(?,?,?)", (name, surname, age))
    db.commit()
    print("done!")
else:
    print("this name also here!")

for data in cursor.execute("SELECT name FROM users"):
    print(data)
