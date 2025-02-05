class Word:
    def __init__(self, base):
        self.base = base

    def generate_word_form(self, word_form_params):
        return self.base

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.base == other.base and self.__class__ == other.__class__
        return False

    def __hash__(self):
        return hash((self.base, self.__class__))