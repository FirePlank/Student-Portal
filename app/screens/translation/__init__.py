from googletrans import Translator
from kivymd.uix.screen import MDScreen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.properties import NumericProperty
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.clock import Clock, mainthread
from kivymd.toast import toast
from functools import partial
import os
import sys
from kivy.lang import Builder
import threading
from ..modules import show_toast
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    return os.path.join(base_path, relative_path)


class Translation(MDScreen):
    with open(resource_path(os.path.join('screens', 'translation', 'langs.json'))) as lang_json:
        langs = json.load(lang_json)
    translator = Translator()

    def __init__(self, **kwargs):
        super().__init__()

        self.from_lang = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.from_lang.bar_inactive_color = self.from_lang.bar_color
        for lang in list(self.langs.keys()):
            btn = DropDownButton(text=lang.title(), size_hint_y=None)
            btn.bind(on_release=lambda btn: self.from_lang.select(btn.text))
            self.from_lang.add_widget(btn)
        self.mainbutton_from_lang = DropDownButton(
            text='Detect Language ↓', size_hint=(0.9, 0.8))
        self.mainbutton_from_lang.bind(on_release=self.from_lang.open)
        self.from_lang.bind(
            on_select=lambda instance,
            x: self.lang_changed(
                self.mainbutton_from_lang,
                x,
                'input'))
        self.ids.from_lang.add_widget(self.mainbutton_from_lang)

        self.to_lang = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.to_lang.bar_inactive_color = self.to_lang.bar_color
        for lang in list(self.langs.keys())[1:]:
            btn = DropDownButton(text=lang.title(), size_hint_y=None)
            btn.bind(on_release=lambda btn: self.to_lang.select(btn.text))
            self.to_lang.add_widget(btn)
        self.mainbutton_to_lang = DropDownButton(
            text='English ↓', size_hint=(0.9, 0.8))
        self.mainbutton_to_lang.bind(on_release=self.to_lang.open)
        self.to_lang.bind(
            on_select=lambda instance,
            x: self.lang_changed(
                self.mainbutton_to_lang,
                x,
                'output'))
        self.ids.to_lang.add_widget(self.mainbutton_to_lang)

    def lang_changed(self, button, text, context):
        setattr(button, 'text', text.title() + ' ↓')
        Clock.schedule_once(lambda dt: self.initiate_translator(), 0)

    def initiate_translator(self, *args):
        self.ids.output_box.text = ''
        try:
            self.realtime_translator.cancel()
        except BaseException:
            pass

        def define_thread(self, text, from_lang, to_lang):
            self.thread = threading.Thread(
                target=self.translate, args=(
                    text, from_lang, to_lang))
            self.thread.daemon = True
            self.translated_text = None
            self.thread.start()
        self.realtime_translator = Clock.schedule_once(lambda dt: define_thread(self, self.ids.input_box.text.strip(
        ), self.mainbutton_from_lang.text[:-2].lower(), self.mainbutton_to_lang.text[:-2].lower()), 1)

    def translate(self, text, from_lang, to_lang):
        if text != '':
            if from_lang == 'detect language' or from_lang is None:
                try:
                    self.translated_text = None
                    self.translated_text = self.translator.translate(
                        text, dest=to_lang).text
                    self.update_output_box()
                except Exception as e:
                    show_toast(
                        'An Error occurred. Check your internet connection.',
                        duration=1)
            else:
                try:
                    self.translated_text = None
                    self.translated_text = self.translator.translate(
                        text, src=from_lang, dest=to_lang).text
                    self.update_output_box()
                except Exception as e:
                    show_toast(
                        'An Error occurred. Check your internet connection.',
                        duration=1)
        else:
            pass

    @mainthread
    def update_output_box(self):
        if self.translated_text:
            self.ids.output_box.text = self.translated_text
        else:
            pass


class DropDownButton(Button, ThemableBehavior, HoverBehavior):
    canvas_opacity = NumericProperty(0)

    def on_enter(self, *args):
        self.canvas_opacity = 1

    def on_leave(self, *args):
        self.canvas_opacity = 0


Builder.load_file('translation.kv')
