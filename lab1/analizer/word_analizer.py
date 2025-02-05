import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

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
        return wordnet.NOUN  # По умолчанию


def analyze_word(word):
    lemmatizer = WordNetLemmatizer()

    # Определяем часть речи
    pos_tag = nltk.pos_tag([word])[0][1]
    wordnet_pos = get_wordnet_pos(pos_tag)

    # Получаем лемму (основу слова)
    lemma = lemmatizer.lemmatize(word, wordnet_pos)

    return {
        "word": word,
        "lemma": lemma,
        "part_of_speech": pos_tag
    }


# Пример использования
word = "going"
result = analyze_word(word)
print(result)
