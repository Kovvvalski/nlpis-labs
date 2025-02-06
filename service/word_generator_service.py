from dto.word_dto import WordDto
from entity.adjective import Adjective
from entity.noun import Noun
from entity.pronoun import Pronoun
from entity.verb import Verb


class WordGeneratorService:
    def generate_word_forms(self, words):
        word_forms = []

        for word in words:
            forms = {}

            # Генерация форм в зависимости от типа слова
            if isinstance(word, Adjective):
                forms["positive"] = word.generate_word_form({"form_type": "positive"})
                forms["comparative"] = word.generate_word_form({"form_type": "comparative"})
                forms["superlative"] = word.generate_word_form({"form_type": "superlative"})

            elif isinstance(word, Noun):
                forms["singular"] = word.generate_word_form({"number": "singular"})
                forms["plural"] = word.generate_word_form({"number": "plural"})
                forms["singular_possessive"] = word.generate_word_form({"number": "singular", "case": "possessive"})
                forms["plural_possessive"] = word.generate_word_form({"number": "plural", "case": "possessive"})

            elif isinstance(word, Pronoun):
                forms["nominative"] = word.generate_word_form({"case": "nominative"})
                forms["accusative"] = word.generate_word_form({"case": "accusative"})
                forms["genitive"] = word.generate_word_form({"case": "genitive"})

            elif isinstance(word, Verb):
                forms["base"] = word.base
                forms["present_third_singular"] = word.generate_word_form({"verb_form": "present_third_singular"})
                forms["gerund"] = word.generate_word_form({"verb_form": "gerund"})
                forms["past"] = word.generate_word_form({"verb_form": "past"})
                forms["participle"] = word.generate_word_form({"verb_form": "participle"})

            # Создаем DTO
            word_forms.append(WordDto(base=word.base, part_of_speech=word.__class__.__name__, forms=forms))

        return word_forms
