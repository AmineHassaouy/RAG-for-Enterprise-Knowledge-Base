import requests
from lxml import html
from .base_loader import BaseLoader
from .document import Document

class WebLoader(BaseLoader):
    def __init__(
            self, 
            timeout=10, 
            headers=None, 
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
            allowed_content_types=None, 
            remove_tags=None
        ):
        self.timeout = timeout
        self.allowed_content_types = [content_type.lower() for content_type in (allowed_content_types if allowed_content_types else ["text/html", "application/xhtml+xml"])]
        self.remove_tags = list(remove_tags) if remove_tags else list(["script", "style"])
        
        self.session = requests.Session()
        base_headers = dict(headers) if headers else {}
        self.session.headers.update(base_headers)
        if user_agent:
            self.session.headers.update({"User-Agent": user_agent})

    def load(self, url):
        html_content = self.fetch(url)
        if not html_content:
            return Document(
                text = "",
                metadata = {
                    "source": url,
                    "type": "web",
                    "title": ""
                }
            )
        
        tree = self.parse(html_content)
        if tree is None:
            return Document(
                            text = "",
                            metadata = {
                                "source": url,
                                "type": "web",
                                "title": ""
                            }
                        )
        
        cleaned_tree = self.clean(tree)
        raw_title = self.extract_title(cleaned_tree)
        raw_text = self.extract_text(cleaned_tree)
        
        return Document(
            text = self.normalize_text(raw_text),
            metadata = {
                "source" : url,
                "type" : "web",
                "title": self.normalize_text(raw_title)
            }
        )
    def fetch(self, url):
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if content_type not in self.allowed_content_types:
                raise ValueError(f"Unsupported content type '{content_type}' for URL: {url}")

            return response.text
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error occurred while fetching {url}") from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out for URL: {url}") from e
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection error while fetching {url}") from e
        except requests.exceptions.TooManyRedirects as e:
            raise RuntimeError(f"Too many redirects while fetching {url}") from e
        except requests.exceptions.RequestException as e:
            raise(f"Request failed for {url}") from e

    def parse(self, html_as_text):
        try:
            return html.fromstring(html_as_text)
        except Exception as e:
            raise ValueError("Failed to parse HTML content.") from e
        
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
        return tree.text_content().strip()
        
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