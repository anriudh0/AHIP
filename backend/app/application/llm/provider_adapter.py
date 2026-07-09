import os
from abc import ABC, abstractmethod
from typing import Type
from .schemas import LLMProviderSettings


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int | None = None) -> dict:
        raise NotImplementedError


_PROVIDER_REGISTRY: dict[str, str] = {
    "mock": "app.application.llm.mock_provider.MockProvider",
}


def _resolve_provider_class(path: str) -> Type[LLMProvider]:
    module_name, class_name = path.rsplit(".", 1)
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


def get_provider(settings: LLMProviderSettings) -> LLMProvider:
    provider_name = settings.provider.lower()
    if provider_name == "mock" or not provider_name:
        provider_class = _resolve_provider_class(_PROVIDER_REGISTRY["mock"])
        return provider_class()

    provider_path = _PROVIDER_REGISTRY.get(provider_name)
    if provider_path is None:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")

    provider_class = _resolve_provider_class(provider_path)
    return provider_class()
