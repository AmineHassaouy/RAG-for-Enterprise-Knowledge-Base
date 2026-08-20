import fitz

def load_pdf(path):
    """
    this function reads a pdf and extracts it's text 
    and preserves metadata (page number) 
    then returns it in a dictionary format (page number + text)
    """
    doc = fitz.open(path)
    text_pages = {}
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        if len(page.get_text().strip()) > 0:
            print(f"Page {page_num+1} contains digital text.")
            print(f"processing pdf pages\n--- Page {page_num+1} ---")
            text_pages[page_num+1] = page.get_text()
        else:
            print(f"Page {page_num+1} is empty or is a scanned image (requires OCR)")
    doc.close
    return text_pages