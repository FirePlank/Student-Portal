import sqlite3
import os



class sql_operator:
    def __init__(self):
        self.PATH = "../app/data/database//user_db.sqlite"

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.PATH, timeout=10)
        except:
            pass
        return connection

    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except:
            pass

    def execute_read_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()

        result = None

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
        except:
            pass
