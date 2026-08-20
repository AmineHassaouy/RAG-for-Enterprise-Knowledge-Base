import requests
from lxml import html

class WebLoader:
    def __init__(
            self, 
            timeout=10, 
            headers=None, 
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
            allowed_content_types=None, 
            remove_tags=None
        ):
        self.timeout = timeout
        self.allowed_content_types = list(allowed_content_types) if allowed_content_types else list(["text/html","application/json"])
        self.remove_tags = list(remove_tags) if remove_tags else list(["script", "style"])
        
        self.session = requests.Session()
        base_headers = dict(headers) if headers else {}
        self.session.headers.update(base_headers)
        if user_agent:
            self.session.headers.update({"User-Agent": user_agent})

    def load(self, url):
        html_content = self.fetch(url)
        if not html_content:
            return {"text": "", "metadata": {"source": url, "title": ""}}
        tree = self.parse(html_content)
        if tree is None:
            return {"text": "", "metadata": {"source": url, "title": ""}}
        cleaned_tree = self.clean(tree)
        raw_title = self.extract_title(cleaned_tree)
        raw_text = self.extract_text(cleaned_tree)
        return {
            "text": self.normalize_text(raw_text),
            "metadata": {
                "source" : url,
                "title": self.normalize_text(raw_title)
            }
        }
    def fetch(self, url):
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.Timeout:
            print("The request timed out!")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.TooManyRedirects as redirect_err:
            print(f"Too many redirects: {redirect_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected request error occurred: {req_err}")
        return None

    def parse(self, html_as_text):
        try:
            tree = html.fromstring(html_as_text)
            return tree
        except Exception as e:
            print(f"Parsing error: {e}")
            return None
        
    def clean(self, tree):
        target_xpath = " | ".join(f"//{tag}" for tag in self.remove_tags)
        if target_xpath:
            for element in tree.xpath(target_xpath):
                element.drop_tree()
        return tree

    def extract_title(self, tree):
        title_selectors = [
            '//h1[contains(@class, "title")]/text()',
            "//h1/text()",
            "//meta[@property='og:title']/@content",
            "//title/text()"
        ]
        for selector in title_selectors:
            result = tree.xpath(selector)
            if result:
                return result[0].strip()
        return ""

    def extract_text(self, tree):
        paragraphs = tree.xpath("//article//p | //main//p | //p")
        paragraphs = list([p.text_content() for p in paragraphs])
        return "\n".join(paragraphs).strip()
        
    def normalize_text(self, text):
        if not text:
            return ""
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            cleaned_line = " ".join(line.split())
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        return "\n\n".join(cleaned_lines)