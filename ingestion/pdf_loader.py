import pymupdf
from pathlib import Path

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
            raw_pages = self.extract_pages(pdf)
            pages = {}
            for num, page in raw_pages.items():
                pages[num] = self.normalize_text(self.extract_text(page))
            return {"pages": pages, "total_pages": len(pages)}
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
        return text.encode(self.encoding, errors="ignore").decode(self.encoding).strip()