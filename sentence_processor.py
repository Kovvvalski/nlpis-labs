import string
from nltk import sent_tokenize, word_tokenize, pos_tag
from word_analyzer import analyze_word


def process_text(text):
    result = []
    sentences = sent_tokenize(text)

    for sentence in sentences:
        sentence_data = {"sentence": sentence, "words": []}
        tokens = word_tokenize(sentence)
        tokens = [token for token in tokens if token not in string.punctuation]
        tagged = pos_tag(tokens)

        for word, tag in tagged:
            semantic_info = analyze_word(word, tag)
            sentence_data["words"].append({
                "word": word,
                "predicates": semantic_info.get_predicates() if semantic_info else ["No predicates recognized"]
            })

        result.append(sentence_data)
    return result
