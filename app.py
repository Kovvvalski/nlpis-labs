from flask import Flask, request, jsonify, render_template

from service.text_extractor_service import TextExtractorService
from service.word_analizer_service import WordAnalyzerService
from service.word_generator_service import WordGeneratorService
from service.corpus_manager_service import CorpusManagerService

app = Flask(__name__)

word_analyzer = WordAnalyzerService()
word_generator = WordGeneratorService()
text_extractor = TextExtractorService()
corpus_manager = CorpusManagerService()


@app.route('/api/process-text', methods=['POST'])
def receive_data():
    data = request.json
    if not isinstance(data, dict) or 'text' not in data:
        return jsonify({"error": "Expected a JSON object with a 'text' field"}), 400

    text = data['text']
    text_format = data['format']
    text = text_extractor.extract(text, text_format)

    if "context" in data and (file_name := data['context']): 
        file_name = file_name.removesuffix('.' + text_format)
        corpus_manager.create_context(text, file_name)
        words = corpus_manager.process_context_text()
    else:
        words = word_analyzer.analyze_text(text)

    word_dto_list = word_generator.generate_word_forms(words)
    return jsonify([word.to_dict() for word in word_dto_list])


@app.route('/api/reload-context', methods=['GET'])
def reload_context():
    try:
        context_words = corpus_manager.process_context_text()
        if not isinstance(context_words, list):  # Ensure array response
            context_words = []
        return jsonify([word.to_dict() for word in context_words])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/find-context', methods=['POST'])
def find_context():
    data = request.json
    if not isinstance(data, dict) or 'phrase' not in data:
        return jsonify({"error": "Missing 'phrase' parameter"}), 400
    
    try:
        results = corpus_manager.find_context(data['phrase'])
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# MVC-контроллер для HTML-страницы
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
