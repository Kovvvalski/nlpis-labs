import spacy
from spacy.cli.download import download
from entity.noun import Noun
from entity.verb import Verb
from entity.adjective import Adjective
from entity.pronoun import Pronoun
from entity.simple_words import *

# Загружаем модель языка для spaCy (например, для английского языка)
try:
    nlp = spacy.load("en_core_web_sm")  # Для других языков используйте соответствующие модели
except IOError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class WordAnalyzerService:
    def __init__(self):
        self.nlp = nlp

    def analyze_word(self, word):
        # Применяем spaCy для обработки слова
        doc = self.nlp(word)
        token = doc[0]  # В spaCy токен - это объект, а не строка

        # Получаем часть речи и лемму
        pos_tag = token.pos_
        lemma = token.lemma_

        # Создаем объект соответствующего класса на основе части речи
        if pos_tag == "NOUN":  # Существительное
            return Noun(lemma)
        elif pos_tag == "VERB":  # Глагол
            return Verb(lemma)
        elif pos_tag == "ADJ":  # Прилагательное
            return Adjective(lemma)
        elif pos_tag == "PRON":  # Местоимение
            return Pronoun(lemma)
        elif pos_tag == "ADP":  # Предлог
            return Preposition(lemma)
        elif pos_tag == "CCONJ":  # Сочинительный союз
            return Conjunction(lemma)
        elif pos_tag == "INTJ":  # Междометие
            return Interjection(lemma)
        elif pos_tag == "DET":  # Артикль, определитель
            return Determiner(lemma)
        elif pos_tag == "PART":  # Частицы
            return Particle(lemma)
        else:
            return None  # Если не удалось определить часть речи

    def analyze_text(self, text, update_repeat_count=False):
        """Modified to support repeat counts"""
        doc = self.nlp(text)
        unique_words = set()
        word_counts = {}

        # First pass: count occurrences
        for token in doc:
            key = token.text.lower()
            word_counts[key] = word_counts.get(key, 0) + 1

        # Second pass: create words with counts
        for token in doc:
            word_obj = self.analyze_word(token.text)
            if word_obj:
                word_obj.repeat_count = word_counts[token.text.lower()]
                unique_words.add(word_obj)

        return unique_words
