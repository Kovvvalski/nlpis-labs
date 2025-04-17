from nltk import pos_tag
from nltk.grammar import CFG, Nonterminal, Production

# Define nonterminals
S = Nonterminal('S')
NP = Nonterminal('NP')
VP = Nonterminal('VP')
PP = Nonterminal('PP')
Det = Nonterminal('Det')
N = Nonterminal('N')
V = Nonterminal('V')
MV = Nonterminal('MV')
Adj = Nonterminal('Adj')
Adv = Nonterminal('Adv')
P = Nonterminal('P')
Pro = Nonterminal('Pro')
Conj = Nonterminal('Conj')

# Lexical tag to grammar category mapping
tag_to_cat = {
    'DT': Det,  # Determiner
    'NN': N,  # Noun (singular)
    'NNS': N,  # Noun (plural)
    'VB': V,  # Verb (base form)
    'VBD': V,  # Verb (past tense)
    'VBN': V,  # Verb (past tense)
    'VBP': V,  # Verb (non-3rd person singular present)
    'VBZ': V,  # Verb (3rd person singular present)
    'VBG': V,  # Verb (gerund/present participle)
    'JJ': Adj,  # Adjective
    'JJR': Adj,  # Adjective (comparative)
    'JJS': Adj,  # Adjective (superlative)
    'RB': Adv,  # Adverb
    'RBR': Adv,  # Adverb (comparative)
    'RBS': Adv,  # Adverb (superlative)
    'IN': P,  # Preposition
    'TO': P,  # Preposition
    'PRP': Pro,  # Pronoun (personal)
    'PRP$': Pro,  # Pronoun (possessive)
    'CC': Conj,  # Coordinating Conjunction
    'MD': MV  # Modal Verb (MV)
}

base_productions = [
    Production(S, [NP, VP]),  # Sentence -> Noun Phrase + Verb Phrase
    Production(VP, [V, NP]),  # Verb Phrase -> Verb + Noun Phrase
    Production(VP, [V]),  # Verb Phrase -> Verb
    Production(VP, [MV]),  # Verb Phrase -> Modal Verb
    Production(VP, [V, NP, PP]),  # Verb Phrase -> Verb + Noun Phrase + Prepositional Phrase
    Production(VP, [MV, V]),  # Verb Phrase -> Modal Verb + Verb
    Production(VP, [V, MV, NP]),  # Verb Phrase -> Verb + Modal Verb + Noun Phrase
    Production(VP, [V, Adv, NP]),  # Verb Phrase -> Verb + Adverb + Noun Phrase
    Production(VP, [V, Pro]),  # Verb Phrase -> Verb + Pronoun
    Production(VP, [Adv, V]),  # Verb Phrase -> Adverb + Verb
    Production(VP, [V, Adv]),  # Verb Phrase -> Verb + Adverb
    Production(VP, [VP, PP]),  # Verb Phrase -> Verb Phrase + Prepositional Phrase
    Production(VP, [VP, Adv]),  # Verb Phrase -> Verb Phrase + Adverb
    Production(NP, [Det, N]),  # Noun Phrase -> Determiner + Noun
    Production(NP, [Det, Adj, N]),  # Noun Phrase -> Determiner + Adjective + Noun
    Production(NP, [NP, PP]),  # Noun Phrase -> Noun Phrase + Prepositional Phrase
    Production(NP, [Pro]),  # Noun Phrase -> Pronoun
    Production(NP, [Pro, Det, N]),  # Noun Phrase -> Pronoun
    Production(NP, [N]),  # Noun Phrase -> Pronoun
    Production(NP, [Adj, N, PP]),  # Noun Phrase -> Adjective + Noun + Prepositional Phrase
    Production(PP, [P, NP]),  # Prepositional Phrase -> Preposition + Noun Phrase
]


def build_grammar(tokens_list) -> CFG:
    terminals = {cat: set() for cat in tag_to_cat.values()}
    productions = base_productions.copy()

    # Lexical analyses
    for tokens in tokens_list:
        tagged = pos_tag(tokens)

        for word, tag in tagged:
            category = tag_to_cat[tag]
            if category:
                terminals[category].add(word)

    for category, words in terminals.items():
        for word in words:
            productions.append(Production(category, [word]))

    # Building grammar
    return CFG(S, productions)

from nltk.grammar import Nonterminal, Production, CFG

def build_productions_from_string(grammar_str):
    productions = []
    start_symbol = None
    for line in grammar_str.strip().splitlines():
        if not line.strip():
            continue
        lhs_rhs = line.split("->")
        if len(lhs_rhs) != 2:
            continue
        lhs = lhs_rhs[0].strip()
        rhs = lhs_rhs[1].strip()
        lhs_symbol = Nonterminal(lhs)
        if start_symbol is None:
            start_symbol = lhs_symbol
        rhs_symbols = []
        for symbol in rhs.split():
            if symbol.startswith("'") and symbol.endswith("'"):
                rhs_symbols.append(symbol.strip("'"))
            else:
                rhs_symbols.append(Nonterminal(symbol))
        productions.append(Production(lhs_symbol, rhs_symbols))
    return CFG(start_symbol, productions)
