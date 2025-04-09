import nltk
from nltk import word_tokenize
import string


def parse_text_tokens(text):
    sentences = nltk.sent_tokenize(text)
    result = {}
    for sent in sentences:
        tokens = word_tokenize(sent.lower())
        tokens = [token for token in tokens if token not in string.punctuation]
        result[sent] = tokens
    return result
