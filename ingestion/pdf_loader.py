import pymupdf
from pathlib import Path
from .document import Document

class PDFLoader:
    def __init__(self,
            extract_images = False,
            preserve_layout = True,
            password = None,
            encoding = 'utf-8'
        ):
        self.extract_images = extract_images
        self.preserve_layout = preserve_layout
        self.password = password
        self.encoding = encoding

    def load(self, path):
        self.validate_file(path)
        pdf = self.open_pdf(path)
        try:
            documents = []

            for num, page in self.extract_pages(pdf).items():
                text = self.normalize_text(self.extract_text(page))
                documents.append(
                    Document(
                        text = text,
                        metadata = {
                            "source" : str(path),
                            "type" : "pdf",
                            "page": num
                        }
                    )
                )
            return documents
        
        finally:
            pdf.close()

    def validate_file(self, path):
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"There is nothing at this path {path}")
        if file_path.suffix.lower() != ".pdf":
            raise ValueError("File must be a PDF.")

    def open_pdf(self, path):
        pdf = pymupdf.open(path)
        if self.password:
            if not pdf.authenticate(self.password):
                raise ValueError(f"Invalid password for {path}.")
        return pdf

    def extract_pages(self, pdf):
        return {i+1: pdf.load_page(i) for i in range(len(pdf))}

    def extract_text(self, page):
        flags = pymupdf.TEXT_PRESERVE_WHITESPACE if self.preserve_layout else 0
        return page.get_text(flags=flags)

    def normalize_text(self, text):
        if not text:
            return ""

        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            clean_line = " ".join(line.split())

            if clean_line:
                cleaned_lines.append(clean_line)
                
        return "\n\n".join(cleaned_lines)