import os
import xml.etree.ElementTree as ET
import spacy
import spacy.cli
import spacy.cli.download
from .word_analizer_service import WordAnalyzerService
from .word_generator_service import WordGeneratorService


class CorpusManagerService:

    def __init__(self) -> None:
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        self.word_registry = {}

    def create_context(self, text: str, file_name: str):
        os.makedirs("xml_context", exist_ok=True)
        doc = self.nlp(text)
        corpus = ET.Element("corpus")

        # Создаем структуру разметки
        sentences_element = ET.SubElement(corpus, "sentences")

        # Размечаем предложения и слова
        for sent_idx, sentence in enumerate(doc.sents, start=1):
            sentence_elem = ET.SubElement(
                sentences_element, "sentence", {"id": str(sent_idx)}
            )

            for token_idx, token in enumerate(sentence, start=1):
                word_elem = ET.SubElement(sentence_elem, "word", {"id": str(token_idx)})
                word_elem.text = token.text  # Токенизация слов [[6]]

        # Сохраняем XML-файл
        tree = ET.ElementTree(corpus)
        tree.write(
            os.path.join("xml_context", file_name + ".xml"),
            encoding="utf-8",
            xml_declaration=True,
        )

    def find_context(self, phrase: str) -> list:
        """Поиск контекста по фразе в сохраненных XML-файлах

        Args:
            phrase (str): Искомая фраза

        Returns:
            list: Список словарей с контекстами и источниками
        """
        results = []
        context_files = self._get_context_files()

        for file_path in context_files:
            
            tree = ET.parse(file_path)
            root = tree.getroot()

            for sentence_elem in root.findall(".//sentence"):
                words = sentence_elem.findall("word")
                sentence_text = ""

                for i, word in enumerate(words):
                    token = word.text

                    if i == 0 or self._is_punctuation(token):
                        sentence_text += token
                    else:
                        sentence_text += " " + token

                if phrase.lower() in sentence_text.lower():
                    results.append(
                        {
                            "found_context": sentence_text.strip(),
                            "source_file": os.path.relpath(file_path),
                        }
                    )

        return results
    
    def process_context_text(self):
        """Process all context files and return analyzed words"""
        self.word_registry = {}
        context_files = self._get_context_files()
        
        for file_path in context_files:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for sentence in root.findall(".//sentence"):
                for word in sentence.findall("word"):
                    word_text = word.text.lower()
                    self.word_registry[word_text] = self.word_registry.get(word_text, 0) + 1
        
        return self._create_word_objects()

    def _get_context_files(self):
        context_dir = "xml_context"
        return [
            os.path.join(context_dir, f) 
            for f in os.listdir(context_dir) 
            if f.endswith(".xml")
        ] if os.path.exists(context_dir) else []

    def _create_word_objects(self):
        analyzer = WordAnalyzerService()
        generator = WordGeneratorService()
        words = []
        
        for word_base, count in self.word_registry.items():
            analyzed = analyzer.analyze_word(word_base)
            if analyzed:
                analyzed.repeat_count = count
                analyzed.fromContext = True  # Add context marker
                # Generate proper DTOs
                words.extend(generator.generate_word_forms([analyzed]))
        
        return words

    @staticmethod
    def _is_punctuation(char: str) -> bool:
        """Проверка, является ли символ знаком препинания"""
        return char in {
            ".",
            ",",
            "!",
            "?",
            ":",
            ";",
            '"',
            "'",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
        }


if __name__ == "__main__":
    text = """
Transport plays a vital role in connecting people, goods, and ideas across the world. From ancient trade routes to modern highways, the movement of individuals and products has shaped economies and cultures throughout history. Today, transportation systems include a wide range of options, such as cars, buses, trains, ships, and airplanes, each serving different needs and distances.

Urban areas rely heavily on public transport, including metros, trams, and buses, to reduce traffic congestion and lower carbon emissions. Meanwhile, long-distance travel often depends on high-speed rail and aviation, enabling fast and efficient movement between cities and countries. Freight transport, essential for global trade, utilizes trucks, cargo ships, and freight trains to deliver goods from manufacturers to consumers.

Technological advancements continue to transform transportation, with electric vehicles, autonomous cars, and hyperloop projects promising cleaner and faster alternatives. Sustainable transport solutions, such as cycling infrastructure and car-sharing programs, are also gaining popularity as cities aim to reduce their environmental impact.

Despite these innovations, challenges remain, including infrastructure maintenance, traffic management, and equitable access to transport services. Governments and private companies must work together to create efficient, affordable, and eco-friendly transportation networks that meet the needs of growing populations.

Ultimately, transport is more than just a way to get from one place to another—it is a cornerstone of modern society, enabling commerce, travel, and social connections on a global scale
    """
    manager = CorpusManagerService()
    print(manager.find_context("transport"))
