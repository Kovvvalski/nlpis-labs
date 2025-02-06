class WordDto:
    def __init__(self, base, part_of_speech, forms):
        self.base = base  # Основная форма слова
        self.part_of_speech = part_of_speech  # Часть речи (Noun, Verb, Adjective и т.д.)
        self.forms = forms  # Словарь с формами слова

    def to_dict(self):
        return {
            "base": self.base,
            "part_of_speech": self.part_of_speech,
            "forms": self.forms
        }
