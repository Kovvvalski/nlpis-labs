from nltk.corpus import wordnet as wn
from semantic_info import SemanticInfo

tags_positions = {
    'J': wn.ADJ,
    'V': wn.VERB,
    'N': wn.NOUN,
    'R': wn.ADV,
}


def analyze_word(word, tag):
    pos = tags_positions.get(tag[0])
    if not pos:
        return None

    synsets = wn.synsets(word, pos=pos)
    if not synsets:
        return None

    semantic_info = SemanticInfo(word)

    for syn in synsets[:1]:
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                semantic_info.add_synonym(lemma.name())

        definition = syn.definition().replace('"', "'")
        semantic_info.add_definition(definition)

        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                semantic_info.add_hypernym(lemma.name())

    return semantic_info
