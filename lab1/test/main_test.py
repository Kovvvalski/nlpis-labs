import unittest
from ..entity.verb import Verb
from ..entity.irregular_verb import IrregularVerb
from ..entity.noun import Noun


class MyTestCase(unittest.TestCase):
    # Тесты для правильных глаголов
    def test_generate_present_third_singular(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "present_third_singular"}), "plays")

        verb2 = Verb("fly", "VB", {})
        self.assertEqual(verb2.generate_word_form({"verb_form": "present_third_singular"}), "flies")

        verb3 = Verb("fix", "VB", {})
        self.assertEqual(verb3.generate_word_form({"verb_form": "present_third_singular"}), "fixes")

        verb4 = Verb("watch", "VB", {})
        self.assertEqual(verb4.generate_word_form({"verb_form": "present_third_singular"}), "watches")

    def test_generate_gerund(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "gerund"}), "playing")

        verb2 = Verb("write", "VB", {})
        self.assertEqual(verb2.generate_word_form({"verb_form": "gerund"}), "writing")

        verb3 = Verb("run", "VB", {})
        self.assertEqual(verb3.generate_word_form({"verb_form": "gerund"}), "running")

        verb4 = Verb("dance", "VB", {})
        self.assertEqual(verb4.generate_word_form({"verb_form": "gerund"}), "dancing")

    def test_generate_past_participle(self):
        verb = Verb("play", "VB", {})
        self.assertEqual(verb.generate_word_form({"verb_form": "participle"}), "played")

        verb2 = Verb("stop", "VB", {})
        self.assertEqual(verb2.generate_word_form({"verb_form": "participle"}), "stopped")

        verb3 = Verb("plan", "VB", {})
        self.assertEqual(verb3.generate_word_form({"verb_form": "participle"}), "planned")

        verb4 = Verb("live", "VB", {})
        self.assertEqual(verb4.generate_word_form({"verb_form": "participle"}), "lived")

    # Тесты для неправильных глаголов
    def test_irregular_verb_past_participle(self):
        irregular_verb = IrregularVerb("go", "VB", {"past": "went", "participle": "gone"})
        self.assertEqual(irregular_verb.generate_word_form({"verb_form": "past"}), "went")
        self.assertEqual(irregular_verb.generate_word_form({"verb_form": "participle"}), "gone")

        irregular_verb2 = IrregularVerb("eat", "VB", {"past": "ate", "participle": "eaten"})
        self.assertEqual(irregular_verb2.generate_word_form({"verb_form": "past"}), "ate")
        self.assertEqual(irregular_verb2.generate_word_form({"verb_form": "participle"}), "eaten")

        irregular_verb3 = IrregularVerb("see", "VB", {"past": "saw", "participle": "seen"})
        self.assertEqual(irregular_verb3.generate_word_form({"verb_form": "past"}), "saw")
        self.assertEqual(irregular_verb3.generate_word_form({"verb_form": "participle"}), "seen")

        irregular_verb4 = IrregularVerb("take", "VB", {"past": "took", "participle": "taken"})
        self.assertEqual(irregular_verb4.generate_word_form({"verb_form": "past"}), "took")
        self.assertEqual(irregular_verb4.generate_word_form({"verb_form": "participle"}), "taken")

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

    def test_generate_plural_noun_irregular(self):
        noun = Noun("man", "NN", {
            "nominative": {"singular": "", "plural": ""},
            "genitive": {"singular": "'s", "plural": "'s"}
        })
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "nominative"}), "man")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "nominative"}), "man")
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "genitive"}), "man's")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "genitive"}), "man's")

    def test_generate_plural_noun_regular(self):
        noun = Noun("cat", "NN", {
            "nominative": {"singular": "", "plural": "s"},
            "genitive": {"singular": "'s", "plural": "s'"}
        })
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "nominative"}), "cat")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "nominative"}), "cats")
        self.assertEqual(noun.generate_word_form({"number": "singular", "case": "genitive"}), "cat's")
        self.assertEqual(noun.generate_word_form({"number": "plural", "case": "genitive"}), "cats'")


if __name__ == '__main__':
    unittest.main()
