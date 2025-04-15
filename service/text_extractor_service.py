import io
from striprtf.striprtf import rtf_to_text
import PyPDF2
from docx import Document

class TextExtractorService:
    def extract(self, file_data, file_extension):
        if file_extension == 'txt':
            return self.extract_text_from_txt(file_data)
        elif file_extension == 'rtf':
            return self.extract_text_from_rtf(file_data)
        elif file_extension == 'pdf':
            return self.extract_text_from_pdf(file_data)
        elif file_extension == 'docx':
            return self.extract_text_from_docx(file_data)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def extract_text_from_txt(self, data):
        return data

    def extract_text_from_rtf(self, data):
        return rtf_to_text(data)

    def extract_text_from_pdf(self, data):
        pdf_file = io.BytesIO(data)
        reader = PyPDF2.PdfReader(pdf_file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return '\n'.join(text)

    def extract_text_from_docx(self, data):
        doc = Document(io.BytesIO(data))
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])