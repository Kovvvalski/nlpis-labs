from nltk import sent_tokenize, word_tokenize, pos_tag
from word_analyzer import analyze_word


def process_text(text):
    result = []
    sentences = sent_tokenize(text)

    for sentence in sentences:
        sentence_data = {"sentence": sentence, "words": []}
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)

        for word, tag in tagged:
            semantic_info = analyze_word(word, tag)
            if semantic_info:
                sentence_data["words"].append({
                    "sentence": sentence,
                    "word": word,
                    "predicates": semantic_info.get_predicates()
                })

        result.append(sentence_data)
    return result
