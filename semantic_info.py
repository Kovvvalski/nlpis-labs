class SemanticInfo:
    def __init__(self, word):
        self.word = word.lower()
        self.synonyms = set()
        self.definitions = []
        self.hypernyms = set()
        self.sentence = ""

    def add_synonym(self, synonym):
        self.synonyms.add(synonym.lower())

    def add_definition(self, definition):
        self.definitions.append(definition)

    def add_hypernym(self, hypernym):
        self.hypernyms.add(hypernym.lower())

    def get_predicates(self):
        predicates = []
        for synonym in self.synonyms:
            predicates.append(f"Synonym({self.word}, {synonym})")
        for definition in self.definitions:
            predicates.append(f"Definition({self.word}, \"{definition}\")")
        for hypernym in self.hypernyms:
            predicates.append(f"Hypernym({self.word}, {hypernym})")
        return sorted(predicates)
