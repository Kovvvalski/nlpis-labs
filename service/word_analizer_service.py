import spacy
from entity.noun import Noun
from entity.verb import Verb
from entity.adjective import Adjective
from entity.pronoun import Pronoun
from entity.simple_words import *

# Загружаем модель языка для spaCy (например, для английского языка)
nlp = spacy.load("en_core_web_sm")  # Для других языков используйте соответствующие модели


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

    def analyze_text(self, text):
        """
        Анализирует текст, токенизирует его и создает объекты классов для слов.
        """
        doc = self.nlp(text)  # spaCy выполняет токенизацию и анализ текста
        unique_words = set()

        for token in doc:
            word_obj = self.analyze_word(token.text)
            if word_obj:
                unique_words.add(word_obj)  # Добавляем объект в множество

        return unique_words
