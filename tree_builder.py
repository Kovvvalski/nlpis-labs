from nltk import EarleyChartParser

def get_trees_for_tokens(sentences_tokens, grammar) -> dict:
    parser = EarleyChartParser(grammar)
    trees_dict = {}
    for sent, tokens in sentences_tokens.items():
        trees = list(parser.parse(tokens))
        trees_dict[sent] = trees if trees else None
    return trees_dict
