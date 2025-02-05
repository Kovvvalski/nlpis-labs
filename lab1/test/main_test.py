import unittest
from ..entity.verb import Verb
from ..entity.irregular_verb import IrregularVerb
from ..entity.noun import Noun


class MyTestCase(unittest.TestCase):
    def test_generate_present_third_singular(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "present_third_singular"}), "plays")

        verb2 = Verb("fly", "VB", {})
        self.assertEqual(verb2.generate_word_form({"verb_form": "present_third_singular"}), "flies")

    def test_generate_gerund(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "gerund"}), "playing")

        verb2 = Verb("write", "VB", {})
        self.assertEqual(verb2.generate_word_form({"verb_form": "gerund"}), "writing")

    def test_generate_past_participle(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "participle"}), "played")

        verb2 = IrregularVerb("write", "VB", {"past": "wrote", "participle": "written"})
        self.assertEqual(verb2.generate_word_form({"verb_form": "participle"}), "written")

    # Тесты для неправильных глаголов
    def test_irregular_verb_past_participle(self):
        irregular_verb = IrregularVerb("go", "VB", {"past": "went", "participle": "gone"})
        self.assertEqual(irregular_verb.generate_word_form({"verb_form": "past"}), "went")
        self.assertEqual(irregular_verb.generate_word_form({"verb_form": "participle"}), "gone")

    # Тесты для существительных
    def test_generate_noun_form(self):
        noun = Noun("dog", "NN", {
            "nominative": {"singular": "", "plural": "s"},
            "genitive": {"singular": "'s", "plural": "s'"}
        })
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "nominative"}), "dog")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "nominative"}), "dogs")
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "genitive"}), "dog's")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "genitive"}), "dogs'")

    def test_generate_irregular_noun_form(self):
        noun = Noun("child", "NN", {
            "nominative": {"singular": "", "plural": "ren"},
            "genitive": {"singular": "'s", "plural": "ren's"}
        })
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "nominative"}), "child")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "nominative"}), "children")
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "genitive"}), "child's")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "genitive"}), "children's")


if __name__ == '__main__':
    unittest.main()
