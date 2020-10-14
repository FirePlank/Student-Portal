from ..modules import sql_operator
from datetime import datetime
from ..widgets.hover_icon_button import HoverIconButton
from kivymd.uix.screen import MDScreen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivymd.toast import toast
from uuid import uuid4


class Notebook(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = NotebookBackend()
        self.initialize_notes()

    def edit_note(self, note_widget):
        if note_widget.ids.edit_button.text == "SAVE":
            note_widget.ids.title.readonly = True
            note_widget.ids.body.readonly = True
            note_widget.ids.delete_button.disabled = False
            note_widget.ids.updatedate_button.disabled = False
            note_widget.ids.title.cursor_blink = False
            note_widget.ids.body.cursor_blink = False
            note_widget.ids.title.text = note_widget.ids.title.text.strip()
            note_widget.ids.body.text = note_widget.ids.body.text.strip()
            note_widget.ids.title.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.body.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.title.background_active = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.body.background_active = 'atlas://data/images/defaulttheme/textinput_active'
            self.database.edit_notes({'unique_id': note_widget.unique_id, 'title': note_widget.ids.title.text, 'body': note_widget.ids.body.text})
            note_widget.ids.edit_button.text = "EDIT"
        elif note_widget.ids.edit_button.text == "EDIT":
            note_widget.ids.title.readonly = False
            note_widget.ids.body.readonly = False
            note_widget.ids.delete_button.disabled = True
            note_widget.ids.updatedate_button.disabled = True
            note_widget.ids.title.cursor_blink = True
            note_widget.ids.body.cursor_blink = True
            note_widget.ids.title.background_normal = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.body.background_normal = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.title.background_active = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.body.background_active = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.edit_button.text = "SAVE"
        else:
            print("[  ERROR  ] Huh? How is this even possible? Smh.")

    def delete_note(self, note_widget):
        self.database.delete_note({'unique_id': note_widget.unique_id})
        self.ids.scroll_box.remove_widget(note_widget)

    def add_note(self):
        added = self.database.add_new_note({'title': '', 'body': ''})
        if added:
            self.initialize_notes()
        else:
            toast('An unexpected error occured.', duration=1)

    def update_date(self, note_widget):
        self.database.update_date({'unique_id': note_widget.unique_id})
        self.initialize_notes()

    def initialize_notes(self):
        self.ids.scroll_box.clear_widgets()
        notes = self.database.show_notes()
        for note in notes:
            note_widget = Note()
            note_widget.ids.title.text = note.get('title')
            note_widget.ids.body.text = note.get('body')
            note_widget.ids.date.text = note.get('create_date')
            note_widget.unique_id = note.get('unique_id')
            self.ids.scroll_box.add_widget(note_widget)
            self.ids.scroller.scroll_y = 1


class Note(FloatLayout):
    unique_id = ""


class NoteButton():
    pass


class NotebookBackend():
    def __init__(self):
        self.OPERATOR = sql_operator()
        create_note_table = """
        CREATE TABLE IF NOT EXISTS notebook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            create_date TEXT NOT NULL
        );
        """
        self.OPERATOR.execute_query(create_note_table)

    def add_new_note(self, data):
        title = data.get('title')
        body = data.get('body')
        unique_id = uuid4()
        creation_time = datetime.now().strftime("%x")
        
        check_existence = f"SELECT unique_id FROM notebook;"

        add_note_in_table = f"""
        INSERT INTO
            notebook (unique_id, title, body, create_date)
        VALUES
            ('{unique_id}', '{title}', '{body}', '{creation_time}');
        """

        id_column = self.OPERATOR.execute_read_query(check_existence)
        id_column = [i[0] for i in id_column] # converting a list of tuple to a list of strings

        if unique_id in id_column:
            return False
        else:
            try:
                self.OPERATOR.execute_query(add_note_in_table)
                return True
            except:
                return False

    def delete_note(self, data):
        unique_id = data["unique_id"]
        delete_query = f"DELETE FROM notebook WHERE unique_id = '{unique_id}'"
        self.OPERATOR.execute_query(delete_query)

    def show_notes(self):
        select_query = "SELECT * FROM notebook"
        notes = self.OPERATOR.execute_read_query(select_query)
        output_list = []

        for i in notes:
            tmp_dict = {
                "unique_id": i[1],
                "title": i[2],
                "body": i[3],
                "create_date": i[4]
            }

            output_list.append(tmp_dict)

        return output_list[::-1]

    def edit_notes(self, data):
        unique_id = data.get("unique_id")
        title = data.get("title")
        body = data.get("body")

        edit_query = f"""
        UPDATE
            notebook
        SET
            body = '{body}',
            title = '{title}'
        WHERE
            unique_id = '{unique_id}'
        """

        self.OPERATOR.execute_query(edit_query)

    def update_date(self, data):
        unique_id = data.get("unique_id")
        creation_time = datetime.now().strftime("%x")

        edit_query = f"""
        UPDATE
            notebook
        SET
            create_date = '{creation_time}'
        WHERE
            unique_id = '{unique_id}'
        """

        self.OPERATOR.execute_query(edit_query)
