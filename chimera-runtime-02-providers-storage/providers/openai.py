from .base import Provider
class OpenAIProvider(Provider):
    def generate(self,prompt): return prompt
