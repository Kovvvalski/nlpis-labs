from flask import Flask, request, Response
from sentence_processor import process_text
import xml.etree.ElementTree as ET

app = Flask(__name__)

def create_xml_response(semantic_info_list):
    root = ET.Element("sentences")

    sentence_map = {}
    for info in semantic_info_list:
        sentence_map.setdefault(info.sentence, []).append(info)

    for sentence_text, words_info in sentence_map.items():
        s_elem = ET.SubElement(root, "sentence", text=sentence_text)

        for info in words_info:
            word_elem = ET.SubElement(s_elem, "word", text=info.word)

            synonyms_elem = ET.SubElement(word_elem, "synonyms")
            for syn in sorted(info.synonyms):
                ET.SubElement(synonyms_elem, "item").text = f"Synonym({info.word}, {syn})"

            definitions_elem = ET.SubElement(word_elem, "definitions")
            for definition in info.definitions:
                ET.SubElement(definitions_elem, "item").text = f'Definition({info.word}, "{definition}")'

            hypernyms_elem = ET.SubElement(word_elem, "hypernyms")
            for hyp in sorted(info.hypernyms):
                ET.SubElement(hypernyms_elem, "item").text = f"Hypernym({info.word}, {hyp})"

    xml_str = ET.tostring(root, encoding="utf-8")
    return Response(xml_str, content_type='application/xml')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return {"error": "Missing 'text' in request"}, 400

    text = data['text']
    result = process_text(text)
    return create_xml_response(result)

if __name__ == '__main__':
    app.run(debug=True)
