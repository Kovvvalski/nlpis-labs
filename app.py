from flask import Flask, request, jsonify
from sentence_processor import process_text

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    text = data['text']
    result = process_text(text)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
