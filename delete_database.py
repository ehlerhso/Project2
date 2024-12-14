import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("DELETE FROM accounts")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'accounts'")
connection.commit()
connection.close()