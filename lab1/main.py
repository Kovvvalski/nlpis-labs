from entity.verb import Verb
from entity.word import Word
from entity.noun import Noun
from entity.irregular_verb import IrregularVerb

# Пример существительных и их окончаний
noun1 = Noun(
    base="dog",
    speech_part="NN",
    forms={
        "nominative": {
            "singular": "",
            "plural": "s"
        },
        "genitive": {
            "singular": "'s",
            "plural": "s'"
        }
    }
)

noun2 = Noun(
    base="child",
    speech_part="NN",
    forms={
        "nominative": {
            "singular": "",
            "plural": "ren"
        },
        "genitive": {
            "singular": "'s",
            "plural": "ren's"
        }
    }
)

noun3 = Noun(
    base="box",
    speech_part="NN",
    forms={
        "nominative": {
            "singular": "",
            "plural": "es"
        },
        "genitive": {
            "singular": "'s",
            "plural": "es'"
        }
    }
)


# Тест 1: Именительный падеж (singular)
assert noun1.generate_word_form({"number": "singular", "case": "nominative"}) == "dog"
assert noun2.generate_word_form({"number": "singular", "case": "nominative"}) == "child"
assert noun3.generate_word_form({"number": "singular", "case": "nominative"}) == "box"

# Тест 2: Именительный падеж (plural)
assert noun1.generate_word_form({"number": "plural", "case": "nominative"}) == "dogs"
assert noun2.generate_word_form({"number": "plural", "case": "nominative"}) == "children"
assert noun3.generate_word_form({"number": "plural", "case": "nominative"}) == "boxes"

# Тест 3: Родительный падеж (singular)
assert noun1.generate_word_form({"number": "singular", "case": "genitive"}) == "dog's"
assert noun2.generate_word_form({"number": "singular", "case": "genitive"}) == "child's"
assert noun3.generate_word_form({"number": "singular", "case": "genitive"}) == "box's"

# Тест 4: Родительный падеж (plural)
assert noun1.generate_word_form({"number": "plural", "case": "genitive"}) == "dogs'"
assert noun2.generate_word_form({"number": "plural", "case": "genitive"}) == "children's"
assert noun3.generate_word_form({"number": "plural", "case": "genitive"}) == "boxes'"
