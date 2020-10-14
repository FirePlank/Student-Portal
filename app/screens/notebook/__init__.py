from ..modules import sql_operator
from datetime import datetime
from ..widgets.hover_icon_button import HoverIconButton
from kivymd.uix.screen import MDScreen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivymd.toast import toast
from kivy.uix.popup import Popup


class Notebook(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = NotebookBackend()
        self.initialize_notes()

    def edit_note(self, note_widget):
        if note_widget.ids.edit_button.text == "SAVE":
            note_widget.ids.body.readonly = True
            note_widget.ids.delete_button.disabled = False
            note_widget.ids.updatedate_button.disabled = False
            note_widget.ids.body.background_color = [133/255, 144/255, 149/255, 0]
            note_widget.ids.body.cursor_blink = False
            note_widget.ids.body.text = note_widget.ids.body.text.strip()
            self.database.edit_notes({'title': note_widget.ids.title.text, 'body': note_widget.ids.body.text})
            note_widget.ids.edit_button.text = "EDIT"
        elif note_widget.ids.edit_button.text == "EDIT":
            note_widget.ids.body.readonly = False
            note_widget.ids.delete_button.disabled = True
            note_widget.ids.updatedate_button.disabled = True
            note_widget.ids.body.background_color = [133/255, 144/255, 149/255, 1]
            note_widget.ids.body.cursor_blink = True
            note_widget.ids.edit_button.text = "SAVE"
        else:
            print("[  ERROR  ] Huh? How is this even possible?")

    def delete_note(self, note_widget):
        self.database.delete_note({'title': note_widget.ids.title.text})
        self.ids.scroll_box.remove_widget(note_widget)

    def add_note(self):
        get_title = NewNotePopup()
        get_title.bind(on_dismiss=lambda a=get_title: self.add_note_popup_closed(a))
        get_title.open()

    def add_note_popup_closed(self, popup):
        title_input = popup.ids.title_input.text.strip()
        if title_input != "":
            added = self.database.add_new_note({'title': popup.ids.title_input.text, 'body': ''})
            if added:
                self.initialize_notes()
            else:
                toast("Note with similar title already exists!", duration=1)

    def update_date(self, note_widget):
        self.database.update_date({'title': note_widget.ids.title.text})
        self.initialize_notes()

    def initialize_notes(self):
        self.ids.scroll_box.clear_widgets()
        notes = self.database.show_notes()
        for note in notes:
            note_widget = Note()
            note_widget.ids.title.text = note.get('title')
            note_widget.ids.body.text = note.get('body')
            note_widget.ids.date.text = note.get('create_date')
            self.ids.scroll_box.add_widget(note_widget)


class Note(FloatLayout):
    pass


class NoteButton():
    pass


class NewNotePopup(Popup):
    pass


class NotebookBackend():
    def __init__(self):
        self.OPERATOR = sql_operator()
        create_note_table = """
        CREATE TABLE IF NOT EXISTS notebook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            create_date TEXT NOT NULL
        );
        """
        self.OPERATOR.execute_query(create_note_table)

    def add_new_note(self, data):
        title = data['title']
        body = data['body']

        creation_time = datetime.now().strftime("%x")
        
        check_existence = f"SELECT title FROM notebook;"

        add_note_in_table = f"""
        INSERT INTO
            notebook (title, body, create_date)
        VALUES
            ('{title}', '{body}', '{creation_time}');
        """

        title_column = self.OPERATOR.execute_read_query(check_existence)
        title_column = [i[0] for i in title_column] # converting a list of tuple to a list of strings

        if title in title_column:
            return False
        else:
            try:
                self.OPERATOR.execute_query(add_note_in_table)
                return True
            except:
                return False

    def delete_note(self, data):
        title = data["title"]
        delete_query = f"DELETE FROM notebook WHERE title = '{title}'"
        self.OPERATOR.execute_query(delete_query)

    def show_notes(self):
        select_query = "SELECT * FROM notebook"
        notes = self.OPERATOR.execute_read_query(select_query)
        output_list = []

        for i in notes:
            tmp_dict = {
                "title": i[1],
                "body": i[2],
                "create_date": i[3]
            }

            output_list.append(tmp_dict)

        return output_list[::-1]

    def edit_notes(self, data):
        title = data.get("title")
        body = data.get("body")

        edit_query = f"""
        UPDATE
            notebook
        SET
            body = '{body}'
        WHERE
            title = '{title}'
        """

        self.OPERATOR.execute_query(edit_query)

    def update_date(self, data):
        title = data.get("title")
        creation_time = datetime.now().strftime("%x")

        edit_query = f"""
        UPDATE
            notebook
        SET
            create_date = '{creation_time}'
        WHERE
            title = '{title}'
        """

        self.OPERATOR.execute_query(edit_query)
