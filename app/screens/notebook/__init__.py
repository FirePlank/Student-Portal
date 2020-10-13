from ..modules import sql_operator
from datetime import datetime


class NotebookBackend():
    def __init__(self):
        self.OPERATOR = sql_operator()

    def add_new_note(self, data):
        title = data['title']
        body = data['body']

        creation_time = datetime.now().strftime("%c")

        ## SQLITE QUERIES ## 

        create_note_table = """
        CREATE TABLE IF NOT EXISTS notebook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            create_date TEXT NOT NULL,
            edit_date TEXT NULL
        );
        """
        
        check_existence = f"SELECT title FROM notebook;"

        add_note_in_table = f"""
        INSERT INTO
            notebook (title, body, create_date)
        VALUES
            ('{title}', '{body}', '{creation_time}');
        """

        self.OPERATOR.execute_query(create_note_table)

        title_column = self.OPERATOR.execute_read_query(check_existence)
        title_column = [i[0] for i in title_column] # converting a list of tuple to a list of strings

        if title in title_column:
            print("Note with similar name already exists!")
        else:
            self.OPERATOR.execute_query(add_note_in_table)

    def delete_previous_note(self, data):
        title = data["title"]
        delete_query = f"DELETE FROM notebook WHERE title = '{title}'"
        self.OPERATOR.execute_query(delete_query)

    def show_notes(self):
        select_query = "SELECT * FROM notebook"
        notes = self.OPERATOR.execute_read_query(select_query)
        for i in notes:
            print(i, type(i))

    def edit_notes(self, data):
        title = data["title"]
        body = data["body"]
        edited_time = datetime.now().strftime("%c")

        edit_query = f"""
        UPDATE
            notebook
        SET
            body = '{body}',
            edit_date = '{edited_time}'
        WHERE
            title = '{title}'
        """

        self.OPERATOR.execute_query(edit_query)
