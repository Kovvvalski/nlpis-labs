from entity.word import Word


class Pronoun(Word):
    def __init__(self, base):
        super().__init__(base)

    def generate_word_form(self, word_form_params):
        case = word_form_params.get("case")

        # Nominative (subject) case pronouns
        nominative = {
            "I": "I", "you": "you", "he": "he", "she": "she", "it": "it", "we": "we", "they": "they"
        }

        # Accusative (object) case pronouns
        accusative = {
            "I": "me", "you": "you", "he": "him", "she": "her", "it": "it", "we": "us", "they": "them"
        }

        # Genitive (possessive) case pronouns
        genitive = {
            "I": "my", "you": "your", "he": "his", "she": "her", "it": "its", "we": "our", "they": "their"
        }

        # Check the case in word_form_params and return the corresponding form
        if case == "nominative":
            return nominative.get(self.base, self.base)
        elif case == "accusative":
            return accusative.get(self.base, self.base)
        elif case == "genitive":
            return genitive.get(self.base, self.base)

        return self.base
