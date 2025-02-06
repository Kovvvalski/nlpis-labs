from striprtf.striprtf import rtf_to_text

class TextExtractorService:
    def extract(self, text, text_format):
        if text_format == 'txt':
            # If the format is 'txt', return the plain text as it is
            return text
        elif text_format == 'rtf':
            # If the format is 'rtf', parse the RTF content to extract the plain text
            return self.extract_text_from_rtf(text)
        else:
            raise ValueError("Unsupported format")

    def extract_text_from_rtf(self, rtf_text):
        """
        Extract plain text from RTF content using the striprtf library.
        """
        return rtf_to_text(rtf_text)
