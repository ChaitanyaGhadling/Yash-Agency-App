import sqlite3


def getConnection():
    return sqlite3.connect('database.db')
