class WordDto:
    def __init__(self, base, part_of_speech, forms, is_exception):
        self.base = base
        self.part_of_speech = part_of_speech
        self.forms = forms
        self.is_exception = is_exception

    def to_dict(self):
        return {
            "base": self.base,
            "part_of_speech": self.part_of_speech,
            "forms": self.forms,
            "is_exception": self.is_exception
        }
