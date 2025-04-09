from flask import Flask, request, jsonify, render_template
from grammar_builder import build_grammar
from tree_builder import get_trees_for_tokens
from parser import parse_text_tokens
import uuid
import os

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_text():
    data = request.get_json()
    text = data.get("text", "")
    sentences_tokens = parse_text_tokens(text)
    grammar = build_grammar(sentences_tokens.values())
    grammar_str = "\n".join(str(prod) for prod in grammar.productions())
    trees_dict = get_trees_for_tokens(sentences_tokens, grammar)
    sentence_data = []

    for sent, trees in trees_dict.items():
        sentence_info = {
            "sentence": sent,
            "trees": []
        }

        if not trees:
            sentence_info["error"] = "Unable to parse this sentence."
            sentence_info["trees"].append(None)
        else:
            for i, tree in enumerate(trees):
                svg = tree._repr_svg_()
                filename = f"static/svg/{uuid.uuid4()}.svg"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(svg)
                sentence_info["trees"].append(filename)

        sentence_data.append(sentence_info)

    return jsonify({
        "grammar": grammar_str,
        "sentences": sentence_data
    })

if __name__ == '__main__':
    os.makedirs("static/svg", exist_ok=True)
    app.run(debug=True)
