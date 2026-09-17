import os
from mistralai.client import Mistral
from indexing.vector_store import SearchResult
from generation.prompt import build_prompt

class AnswerGenerator:

    def __init__(self, model = "mistral-small-lattest"):
        api_key = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=api_key)
        self.model = model

    def generate(self, query, results):

        prompt = build_prompt(query=query, results=results)

        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt,}
            ],
        )

        return response.choices[0].message.content