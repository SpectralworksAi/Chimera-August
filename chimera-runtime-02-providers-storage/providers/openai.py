import os
from openai import OpenAI

from .base import Provider


class OpenAIProvider(Provider):
    """Real OpenAI provider for the CHIMERA provider interface."""

    def __init__(self, model=None, client=None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.6")
        self.client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
