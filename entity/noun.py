import inflect
from entity.word import Word

class Noun(Word):
    def __init__(self, base):
        super().__init__(base)
        self.inflector = inflect.engine()

    def generate_word_form(self, word_form_params):
        """
        Generates the word form based on given parameters like number (singular/plural)
        and case (nominative, possessive, etc.).
        """
        number = word_form_params.get('number', 'singular')
        case = word_form_params.get('case', 'nominative')

        # Pluralization
        if number == 'plural':
            noun_form = self.inflector.plural(self.base)
        else:
            noun_form = self.base

        # Possessive case
        if case == 'possessive':
            if noun_form.endswith('s'):
                noun_form += "'"
            else:
                noun_form += "'s"

        return noun_form
