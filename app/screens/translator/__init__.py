from googletrans import Translator


class Translation:
    def __init__(self, text, from_lang=None, to_lang="en"):
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self):
        if self.from_lang is None:
            return Translator().translate(self.text, dest=self.to_lang).text
        else:
            return Translator().translate(self.text, src=self.from_lang, dest=self.to_lang).text