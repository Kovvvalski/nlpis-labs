import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

from lab1.entity.noun import Noun
from lab1.entity.verb import Verb
from lab1.entity.adjective import Adjective
from lab1.entity.pronoun import Pronoun
from lab1.entity.simple_words import *

# Функция для получения части речи в формате WordNet
def get_wordnet_pos(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None  # Игнорируем ненужные части речи


class WordAnalyzer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def analyze_word(self, word):
        pos_tag = nltk.pos_tag([word])[0][1]
        wordnet_pos = get_wordnet_pos(pos_tag)
        lemma = self.lemmatizer.lemmatize(word, wordnet_pos) if wordnet_pos else self.lemmatizer.lemmatize(word,
                                                                                                           wordnet.VERB)

        # Создаем объект соответствующего класса
        if pos_tag.startswith("NN"):  # Noun (существительное)
            return Noun(lemma)
        elif pos_tag.startswith("VB"):  # Verb (глагол)
            return Verb(lemma)
        elif pos_tag.startswith("JJ"):  # Adjective (прилагательное)
            return Adjective(lemma)
        elif pos_tag.startswith("PRP"):  # Pronoun (местоимение)
            return Pronoun(lemma)
        elif pos_tag.startswith("IN"):  # Prepositions (предлог)
            return Preposition(lemma)
        elif pos_tag.startswith("CC"):  # Conjunctions (союз)
            return Conjunction(lemma)
        elif pos_tag.startswith("UH"):  # Interjections (междометие)
            return Interjection(lemma)
        elif pos_tag.startswith("DT"):  # Determiners (определители)
            return Determiner(lemma)
        elif pos_tag.startswith("RP"):  # Particles (частицы)
            return Particle(lemma)
        else:
            return None  # Если слово не подходит, игнорируем его

    def analyze_text(self, text):
        """
        Анализирует текст, токенизирует его и создает объекты классов для слов.
        """
        words = word_tokenize(text)  # Токенизация текста
        unique_words = set()

        for word in words:
            word_obj = self.analyze_word(word)
            if word_obj:
                unique_words.add(word_obj)  # Добавляем объект в множество

        return unique_words
