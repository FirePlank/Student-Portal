from ..modules import sql_operator
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty
from ..widgets.hover_icon_button import HoverIconButton
from ..widgets.hover_flat_button import HoverFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.toast import toast
from kivy.lang import Builder
from ..widgets.custom_scroll import CustomScroll


class ToDo(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = ToDoBackend()
        self.initialize_tasks()

    def initialize_tasks(self):
        self.ids.scroll_box.clear_widgets()
        tasks = self.database.show_item()
        for task in tasks:
            task_widget = Task()
            task_widget.ids.title.text = task.get('item')
            task_widget.unique_id = task.get('id')
            task_widget.status = task.get('status')
            self.ids.scroll_box.add_widget(task_widget)
            self.ids.scroller.scroll_y = 1

    def delete_task(self, task_widget):
        self.database.delete_item(task_widget.unique_id)
        self.initialize_tasks()
        toast('Task deleted.', duration=0.3)

    def add_task(self):
        added = self.database.add_item('', 0)
        if added:
            self.initialize_tasks()
            toast('Task Created.', duration=0.3)
        else:
            toast('Cannot add task.', duration=1)

    def update_status(self, task_widget):
        if task_widget.status:
            task_widget.status = 0
            self.database.update_item_status(task_widget.unique_id, 0)
        elif not task_widget.status:
            task_widget.status = 1
            self.database.update_item_status(task_widget.unique_id, 1)
        else:
            print("How is this even possible eh? smh.")

    def edit_task(self, task_widget):
        if task_widget.ids.edit_button.text == "EDIT TASK":
            task_widget.ids.title.readonly = False
            task_widget.ids.delete_button.disabled = True
            task_widget.ids.title.cursor_blink = True
            task_widget.ids.edit_button.text = "SAVE"
        else:
            task_widget.ids.title.readonly = True
            task_widget.ids.delete_button.disabled = False
            task_widget.ids.title.cursor_blink = False
            task_widget.ids.title.text = task_widget.ids.title.text.strip()
            self.database.update_item_content(
                task_widget.unique_id, task_widget.ids.title.text)
            task_widget.ids.edit_button.text = "EDIT TASK"
            toast('Note data saved.', duration=0.3)

    def cleanup(self):
        for task_widget in self.ids.scroll_box.children:
            if task_widget.ids.edit_button.text == "SAVE":
                task_widget.ids.title.readonly = True
                task_widget.ids.delete_button.disabled = False
                task_widget.ids.title.cursor_blink = False
                task_widget.ids.edit_button.text = "EDIT"
        self.initialize_tasks()


class Task(MDGridLayout):
    status = NumericProperty()


class ToDoBackend():
    def __init__(self):
        self.OPERATOR = sql_operator()
        create_todo_table = """
        CREATE TABLE IF NOT EXISTS todo (
            unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            status INTEGER NOT NULL
        )
        """

        self.OPERATOR.execute_query(create_todo_table)

    def add_item(self, item, status):
        add_item_query = f"""
        INSERT INTO
            todo (item, status)
        VALUES
            ('{item}', '{status}')
        """
        try:
            self.OPERATOR.execute_query(add_item_query)
            return True
        except BaseException:
            return False

    def delete_item(self, unique_id):
        delete_query = f"DELETE FROM todo WHERE unique_id = ({unique_id})"

        try:
            self.OPERATOR.execute_query(delete_query)
            return True
        except BaseException:
            return False

    def show_item(self):
        show_query = f"SELECT * FROM todo"
        try:
            items = self.OPERATOR.execute_read_query(show_query)
        except BaseException:
            items = []

        output_data = []

        for item in items:
            tmp_data = {
                "id": item[0],
                "item": item[1],
                "status": item[2]
            }

            output_data.append(tmp_data)

        return output_data

    def update_item_content(self, unique_id, title):
        edit_query = f"""
        UPDATE
            todo
        SET
            item = '{title}'
        WHERE
            unique_id = '{unique_id}'
        """

        self.OPERATOR.execute_query(edit_query)

    def update_item_status(self, unique_id, status):
        edit_query = f"""
        UPDATE
            todo
        SET
            status = '{int(status)}'
        WHERE
            unique_id = '{unique_id}'
        """

        self.OPERATOR.execute_query(edit_query)


Builder.load_file('todo.kv')
