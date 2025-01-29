import sqlite3


def initialize():
    conn = sqlite3.connect('local.db')
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name VARCHAR(50), age INTEGER)''')

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect('local.db')
