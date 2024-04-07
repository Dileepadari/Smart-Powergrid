import sqlite3


def get_info(query):
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    result = curser.execute(query)
    data = result.fetchall()
    return data

