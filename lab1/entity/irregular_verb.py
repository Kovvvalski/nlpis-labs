from .verb import Verb


class IrregularVerb(Verb):
    def generate_word_form(self, word_form_params):
        form = word_form_params.get("verb_form")
        if form in ["past", "participle"]:
            return self.forms[form]
        return super().generate_word_form(word_form_params)
