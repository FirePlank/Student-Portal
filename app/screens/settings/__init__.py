from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from ..modules import sql_operator, string_to_list



class Settings(MDScreen):
	pass


class SettingsBackend:
	def __init__(self):
		self.OPERATOR = sql_operator()
		create_settings_table = """
		CREATE TABLE IF NOT EXISTS settings_data(
			bg_color TEXT NOT NULL,
			tile_color TEXT NOT NULL,
			raised_button_color TEXT NOT NULL,
			text_color TEXT NOT NULL,
			title_text_color TEXT NOT NULL,
			accent_color TEXT NOT NULL,
			theme TEXT NOT NULL,
			page_transition NOT NULL
		)
		"""
		default_value = """
		INSERT INTO
			settings_data(bg_color, tile_color, raised_button_color, text_color, title_text_color, accent_color, theme, page_transition)
		VALUES
			("[71/255, 93/255, 102/255, 1]", "[133/255, 144/255, 149/255, 1]", "[144/255, 159/255, 165/255, 1]", "[0, 0, 0, 1]", "[1, 1, 1, 1]", "[0.5, 0.7, 0.5, 1]", "dark", "slide") 
		"""

		self.OPERATOR.execute_query(create_settings_table)
		self.OPERATOR.execute_query(default_value)

	def show_settings(self):
		show_table_date = "SELECT * FROM settings_data"
		data = self.OPERATOR.execute_read_query(show_table_date)[0]

		output_data = {
			"bg_color" : string_to_list(data[0]),
			"tile_color" : string_to_list(data[1]),
			"raised_button_color" : string_to_list(data[2]),
			"text_color" : string_to_list(data[3]),
			"title_text_color" : string_to_list(data[4]),
			"accent_color" : string_to_list(data[5]),
			"theme" : data[6],
			"page_transition" : data[7]
		}

		return output_data

	def edit_settings(self, key, value):
		update_query = f"""
		UPDATE
			settings_data
		SET
			{key} = '{value}'
		"""

		self.OPERATOR.execute_query(update_query)



Builder.load_file('settings.kv')
