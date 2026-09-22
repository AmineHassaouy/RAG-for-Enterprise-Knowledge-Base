import os

from dotenv import load_dotenv
from mistralai.client import Mistral

from indexing.vector_store import SearchResult
from generation.prompt import build_prompt
from mistralai.client.errors.sdkerror import SDKError

load_dotenv()


class AnswerGenerator:

    def __init__(
        self,
        model: str = "mistral-small-latest",
    ):
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY environment variable is not set."
            )

        self.client = Mistral(api_key=api_key)
        try:
            models_response = self.client.models.list()
            available_models = [model.id for model in models_response.data]

        except SDKError as e:
            if e.status_code == 401:
                raise ValueError("MISTRAL_API_KEY is invalid (unauthorized 401)") from e
            elif e.status_code == 429:
                raise PermissionError(
                    "Rate limit or Account restriction exceeded (429)"
                ) from e
            else:
                raise RuntimeError(f"Mistral API error (Status {e.status_code}): {e.message}") from e
            
        if model in available_models:
            self.model = model
        else:
            raise ValueError(
                f"The provided model \"{model}\" isn't available for this account. "
                f"Available models: {available_models}"
            )

    def generate(
        self,
        query: str,
        results: list[SearchResult],
    ) -> str:

        if not query.strip():
            return ""

        try:
            prompt = build_prompt(
                query=query,
                results=results,
            )
        except Exception as e:
            raise ValueError(
                f"Error while constructing RAG prompt (verify 'results' structure): {str(e)}"
            ) from e

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        except SDKError as e:
            if e.status_code == 429:
                raise PermissionError(
                    "Rate limit or Account restriction exceeded (429)"
                ) from e
            elif e.status_code == 400:
                raise ValueError(
                    f"Invalid request (400). the combined volume of the result documents and the query likely exceeds the maximum capacity of the model {self.model}. Details: {e.message}"
                ) from e
            elif e.status_code >= 500:
                raise RuntimeError(
                    f"Mistral server outage or overload (Status {e.status_code}). Please try again"
                ) from e
            else:
                raise RuntimeError(
                    f"Unhandled Mistral API error (Status {e.status_code}): {e.message}"
                ) from e
        except Exception as e:
            raise ConnectionError(
                f"Unable to reach the Mistral API (local network issue). Details: {str(e)}"
            ) from e

        return response.choices[0].message.content