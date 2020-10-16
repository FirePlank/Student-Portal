import sqlite3
from sqlite3 import Error
import os
import sys
from kivymd.app import MDApp

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class sql_operator:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            user_data_dir = getattr(MDApp.get_running_app(), 'user_data_dir')
            self.PATH = resource_path(os.path.join(os.path.dirname(user_data_dir), 'Student Portal', 'database'))
            if not os.path.isdir(self.PATH):
                os.makedirs(self.PATH)
            self.PATH = os.path.join(self.PATH, 'user_db.sqlite')
            print(self.PATH)
        else:
            self.PATH = os.path.join('data', 'database', 'user_db.sqlite')

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.PATH, timeout=10)
            print("Connected successfully")
        except Error as e:
            print(e)
        return connection

    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Executed the query successfully")
        except Error as e:
            print(e)

    def execute_read_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()

        result = None

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            print("Executed the read query successfully")
            return result
        except Error as e:
            print(e)
