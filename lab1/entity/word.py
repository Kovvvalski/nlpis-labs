class Word:
    def __init__(self, base, speech_part, forms):
        self.base = base  # The base form of the word
        self.speech_part = speech_part  # Part of speech (noun, verb, etc.)
        self.forms = forms  # Dictionary or list of endings

    def generate_word_form(self, word_form_params):
        return self.base

    def get_speech_part(self):
        return self.speech_part
