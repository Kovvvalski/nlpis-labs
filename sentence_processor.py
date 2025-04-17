import string
from nltk import sent_tokenize, word_tokenize, pos_tag
from word_analyzer import analyze_word

def process_text(text):
    semantic_info_list = []
    sentences = sent_tokenize(text)

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tokens = [token for token in tokens if token not in string.punctuation]
        tagged = pos_tag(tokens)

        for word, tag in tagged:
            semantic_info = analyze_word(word, tag)
            if semantic_info:
                semantic_info.sentence = sentence  # добавим контекст предложения
                semantic_info_list.append(semantic_info)

    return semantic_info_list
