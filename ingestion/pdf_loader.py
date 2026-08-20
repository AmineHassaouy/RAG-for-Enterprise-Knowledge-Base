import pymupdf
from pathlib import Path
import json

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
        if self.validate_file(path):
            pdf = self.open_pdf(path)
            pages = self.extract_pages(pdf)
            for num, page in pages.items():
                pages[num] = self.extract_text(page)
            return {"pages with their numbers": pages,
                    "number of pages": len(pages)}

    def validate_file(self, path):
        if Path(path).exists():
            if Path(path).is_file():
                if Path(path).suffix.lower() == ".pdf":
                    print("Valid pdf path.")
                    return True
                else:
                    print("This file isn't supported please enter a pdf.")
                    return
            else:
                print("This is not a file path please enter a pdf file.")
                return
        else:
            print("Please enter a valid path.")
            return

    def open_pdf(self, path):
        pdf = pymupdf.open(path)
        return pdf

    def extract_pages(self, pdf: pymupdf.Document):
        pages = {}
        for page_num in range(len(pdf)):
            pages[page_num+1] = pdf.load_page(page_num)
        return pages

    def extract_text(self, page: pymupdf.Page):
        return page.get_text()

    def normalize_text(self, text):
        pass

pdf_loader = PDFLoader()
print(pdf_loader.load("ingestion/exemple 1.pdf"))