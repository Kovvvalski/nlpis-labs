from entity.word import Word


class Adjective(Word):

    def generate_word_form(self, word_form_params):
        form_type = word_form_params.get("form_type")

        if form_type == "positive":
            # Base form is the adjective itself
            return self.base

        elif form_type == "comparative":
            # For comparative form
            if self.base.endswith('y'):
                return self.base[:-1] + 'ier'
            elif len(self.base) > 2 and self.base[-1] in 'e':
                return self.base + 'r'
            return self.base + 'er'

        elif form_type == "superlative":
            # For superlative form
            if self.base.endswith('y'):
                return self.base[:-1] + 'iest'
            elif len(self.base) > 2 and self.base[-1] in 'e':
                return self.base + 'st'
            return self.base + 'est'

        return self.base
