from googletrans import Translator
from kivymd.uix.screen import MDScreen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.properties import NumericProperty
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.clock import Clock
from kivymd.toast import toast
from functools import partial
import os


class Translation(MDScreen):
    langs = {
        'detect language': '',
        'afrikaans': '',
        'albanian': '',
        'amharic': '',
        'arabic': '',
        'armenian': '',
        'azerbaijani': '',
        'basque': '',
        'belarusian': '',
        'bengali': '',
        'bosnian': '',
        'bulgarian': '',
        'catalan': '',
        'cebuano': '',
        'chichewa': '',
        'chinese (simplified)': '',
        'chinese (traditional)': '',
        'corsican': '',
        'croatian': '',
        'czech': '',
        'danish': '',
        'dutch': '',
        'english': '',
        'esperanto': '',
        'estonian': '',
        'filipino': '',
        'finnish': '',
        'french': '',
        'frisian': '',
        'galician': '',
        'georgian': '',
        'german': '',
        'greek': '',
        'gujarati': '',
        'haitian creole': '',
        'hausa': '',
        'hawaiian': '',
        'hebrew': '',
        'hebrew': '',
        'hindi': '',
        'hmong': '',
        'hungarian': '',
        'icelandic': '',
        'igbo': '',
        'indonesian': '',
        'irish': '',
        'italian': '',
        'japanese': '',
        'javanese': '',
        'kannada': '',
        'kazakh': '',
        'khmer': '',
        'korean': '',
        'kurdish (kurmanji)': '',
        'kyrgyz': '',
        'lao': '',
        'latin': '',
        'latvian': '',
        'lithuanian': '',
        'luxembourgish': '',
        'macedonian': '',
        'malagasy': '',
        'malay': '',
        'malayalam': '',
        'maltese': '',
        'maori': '',
        'marathi': '',
        'mongolian': '',
        'myanmar (burmese)': '',
        'nepali': '',
        'norwegian': '',
        'odia': '',
        'pashto': '',
        'persian': '',
        'polish': '',
        'portuguese': '',
        'punjabi': '',
        'romanian': '',
        'russian': '',
        'samoan': '',
        'scots gaelic': '',
        'serbian': '',
        'sesotho': '',
        'shona': '',
        'sindhi': '',
        'sinhala': '',
        'slovak': '',
        'slovenian': '',
        'somali': '',
        'spanish': '',
        'sundanese': '',
        'swahili': '',
        'swedish': '',
        'tajik': '',
        'tamil': '',
        'telugu': '',
        'thai': '',
        'turkish': '',
        'ukrainian': '',
        'urdu': '',
        'uyghur': '',
        'uzbek': '',
        'vietnamese': '',
        'welsh': '',
        'xhosa': '',
        'yiddish': '',
        'yoruba': '',
        'zulu': '',
    }
    translator = Translator()
    def __init__(self, **kwargs):
        super().__init__()
        from .. import resource_path
        self.resource_path = resource_path

        from_lang = DropDown(bar_width=10, scroll_type=['bars', 'content'], effect_cls='ScrollEffect', smooth_scroll_end=10)
        from_lang.bar_inactive_color = from_lang.bar_color
        for lang in list(self.langs.keys()):
            btn = DropDownButton(text=lang.title(), size_hint_y=None)
            btn.bind(on_release=lambda btn: from_lang.select(btn.text))
            from_lang.add_widget(btn)
        self.mainbutton_from_lang = DropDownButton(text='Detect Language ↓', size_hint=(0.9, 0.8))
        self.mainbutton_from_lang.bind(on_release=from_lang.open)
        from_lang.bind(on_select=lambda instance, x: self.lang_changed(self.mainbutton_from_lang, x, 'input'))
        self.ids.from_lang.add_widget(self.mainbutton_from_lang)
        self.mainbutton_from_lang.pos_x = self.mainbutton_from_lang.parent.width-self.mainbutton_from_lang.width - 5

        to_lang = DropDown(bar_width=10, scroll_type=['bars', 'content'], effect_cls='ScrollEffect', smooth_scroll_end=10)
        to_lang.bar_inactive_color = to_lang.bar_color
        for lang in list(self.langs.keys())[1:]:
            btn = DropDownButton(text=lang.title(), size_hint_y=None)
            btn.bind(on_release=lambda btn: to_lang.select(btn.text))
            to_lang.add_widget(btn)
        self.mainbutton_to_lang = DropDownButton(text='English ↓', size_hint=(0.9, 0.8))
        self.mainbutton_to_lang.bind(on_release=to_lang.open)
        to_lang.bind(on_select=lambda instance, x: self.lang_changed(self.mainbutton_to_lang, x, 'output'))
        self.ids.to_lang.add_widget(self.mainbutton_to_lang)

    def lang_changed(self, button, text, context):
        setattr(button, 'text', text.title()+' ↓')
        Clock.schedule_once(lambda dt: self.initiate_translator(), 0)

    def initiate_translator(self, *args):
        self.ids.output_box.text = ''
        try:
            self.realtime_translator.cancel()
        except Exception as e:
            print(e)
        self.realtime_translator = Clock.schedule_once(partial(self.translate, self.ids.input_box.text.strip(), self.mainbutton_from_lang.text[:-2].lower(), self.mainbutton_to_lang.text[:-2].lower()), 1)

    def translate(self, text, from_lang, to_lang, dt):
        if text != '':
            if from_lang == 'detect language' or from_lang == None:
                try:
                    self.ids.output_box.text = self.translator.translate(text, dest=to_lang).text
                except Exception as e:
                    toast('An Error occured. Check your internet connection.\n' + f'Error: {str(e)}'.center(max(len(f'Error: {str(e)}'), len('An Error occured. Check your internet connection.'))), duration=5)
            else:
                try:
                    self.ids.output_box.text = self.translator.translate(text, src=from_lang, dest=to_lang).text
                except Exception as e:
                    toast('An Error occured. Check your internet connection.\n' + f'Error: {str(e)}'.center(max(len(f'Error: {str(e)}'), len('An Error occured. Check your internet connection.'))), duration=5)
        else:
            self.ids.output_box.text = ""


class DropDownButton(Button, ThemableBehavior, HoverBehavior):
    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0
