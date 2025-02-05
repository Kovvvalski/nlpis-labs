from .word import Word

class Noun(Word):
    def generate_word_form(self, word_form_params):
        """
        Generates the word form based on given parameters like number (singular/plural)
        and case (nominative, genitive, etc.).
        form_params should include 'number' (singular/plural) and 'case' (e.g., nominative, genitive).
        """
        number, case = word_form_params['number'], word_form_params['case']
        return self.base + self.forms[case][number]
