import os

from openai import OpenAI

from .openai import OpenAIProvider


class FakeResponses:
    def create(self, **kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["input"] == "hello"
        return type("Response", (), {"output_text": "world"})()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_openai_provider_uses_responses_api(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    provider = OpenAIProvider(model="test-model", client=FakeClient())
    assert provider.generate("hello") == "world"
