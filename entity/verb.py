from entity.word import Word

VOWELS = 'aeiouy'

class Verb(Word):
    def generate_word_form(self, word_form_params):
        form = word_form_params.get("verb_form")
        if form == "present_third_singular":
            return self._generate_present_third_singular()
        elif form == "gerund":
            return self._generate_gerund()
        elif form in ["past", "participle"]:
            return self._generate_past_participle()
        else:
            return self.base

    def _generate_present_third_singular(self):
        if self.base.endswith('y') and not self.base[-2] in VOWELS:  # "y" preceded by consonant
            return self.base[:-1] + 'ies'
        elif self.base.endswith(('o', 'ch', 's', 'sh', 'x')):  # "o", "ch", "s", "sh", "x" add "es"
            return self.base + 'es'
        return self.base + 's'  # Default case: add "s"

    def _generate_gerund(self):
        if self.base.endswith('e'):  # Case 1: If ends with "e", remove "e" and add "ing"
            return self.base[:-1] + 'ing'
        if len(self.base) > 2 and self.base[-1] not in VOWELS and self.base[-2] in VOWELS and self.base[-3] not in VOWELS:  # Case 2: Double the final consonant before adding "ing"
            return self.base + self.base[-1] + 'ing'
        return self.base + 'ing'  # Default case: just add "ing"

    def _generate_past_participle(self):
        if self.base.endswith('e'):  # Case 1: If ends with "e" add "d"
            return self.base + 'd'
        if len(self.base) > 2 and self.base[-1] not in VOWELS and self.base[-2] in VOWELS and self.base[-3] not in VOWELS:  # Case 2: Double the final consonant before adding "ed"
            return self.base + self.base[-1] + 'ed'
        return self.base + 'ed'  # Default case: just add "ed"
