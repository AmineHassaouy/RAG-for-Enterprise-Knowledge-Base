import os
from mistralai.client import Mistral
from indexing.vector_store import SearchResult
from generation.prompt import build_prompt

class AnswerGenerator:

    def __init__(self, model: str = "mistral-small-lattest"):
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError("MISTRAL_API_KEY isnt set!")

        self.client = Mistral(api_key=api_key)
        self.model = model

    def generate(self, query: str, results: list[SearchResult]) -> str:
        if not query.strip():
            return ""

        prompt = build_prompt(query=query, results=results)

        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt,}
            ],
        )

        return response.choices[0].message.content