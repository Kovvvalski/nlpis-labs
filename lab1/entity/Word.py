from abc import ABC, abstractmethod

class Word(ABC):
    def __init__(self, base):
        self.word = base

    @abstractmethod
    def generate_word_form(self, form_params):
        pass
