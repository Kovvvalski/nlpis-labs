from flask import Flask, request, jsonify, render_template

from service.text_extractor_service import TextExtractorService
from service.word_analizer_service import WordAnalyzerService
from service.word_generator_service import WordGeneratorService

app = Flask(__name__)

word_analyzer = WordAnalyzerService()
word_generator = WordGeneratorService()
text_extractor = TextExtractorService()


@app.route('/api/process-text', methods=['POST'])
def receive_data():
    data = request.json
    if not isinstance(data, dict) or 'text' not in data:
        return jsonify({"error": "Expected a JSON object with a 'text' field"}), 400

    text = data['text']
    text_format = data['format']
    text = text_extractor.extract(text, text_format)
    words = word_analyzer.analyze_text(text)
    word_dto_list = word_generator.generate_word_forms(words)
    return jsonify([word.to_dict() for word in word_dto_list])


# MVC-контроллер для HTML-страницы
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
