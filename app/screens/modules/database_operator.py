import sqlite3
from sqlite3 import Error
import os

class sql_operator:
    def __init__(self):
        self.PATH = "../app/data/database//user_db.sqlite"
    
    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.PATH)
            print("successfully connected to the DB")
        except Error as e:
            print(e)
        return connection

    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("executed query successfully")
        except Error as e:
            print(error)
    
    def execute_read_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()

        result = None

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(e)
    