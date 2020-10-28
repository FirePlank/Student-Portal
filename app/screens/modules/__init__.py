import sqlite3
from sqlite3 import Error
import os
from kivymd.app import MDApp


def string_to_list(data_in):
    data_out = data_in.replace('[', '').replace(']', '')
    data_out = data_out.split(', ')
    to_parse = data_out
    parsed = []
    for i in to_parse:
        try:
            parsed.append(float(i))
        except:
            try:
                num, denom = i.split('/')
                parsed.append(float(num)/float(denom))
            except Exception as e:
                print(e)
    return parsed

class sql_operator:
    def __init__(self):
        user_data_dir = getattr(MDApp.get_running_app(), 'user_data_dir')
        self.PATH = os.path.join(os.path.dirname(user_data_dir), 'Student Portal', 'database')
        if not os.path.isdir(self.PATH):
            os.makedirs(self.PATH)
        self.PATH = os.path.join(self.PATH, 'user_db.sqlite')

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.PATH, timeout=10)
        except Error as e:
            print(e)
            print(self.PATH)
        return connection

    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
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
            return result
        except Error as e:
            print(e)
