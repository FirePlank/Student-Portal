from ..modules import sql_operator



class ToDoBackend():
    def __init__(self):
        self.OPERATOR = sql_operator()
        create_todo_table = """
        CREATE TABLE IF NOT EXISTS todo (
            unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL
        )
        """

        self.OPERATOR.execute_query(create_todo_table)

    def add_item(self, item):
        add_item_query = f"""
        INSERT INTO
            todo(item)
        VALUES
            ('{item}')
        """
        try:
            self.OPERATOR.execute_query(add_item_query)
            return True
        except:
            return False

    def delete_item(self, unique_id):
        delete_query = f"DELETE FROM todo WHERE unique_id = ({unique_id})"

        try:
            self.OPERATOR.execute_query(delete_query)
            return True
        except:
            return False

    def show_item(self):
        show_query = f"SELECT * FROM todo"
        try:
            items = self.OPERATOR.execute_read_query(show_query)
        except:
            items = []

        output_data = []

        for item in items:
            tmp_data = {
                "id": item[0],
                "item": item[1]
            }

            output_data.append(tmp_data)

        return output_data
