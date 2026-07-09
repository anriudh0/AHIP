from __future__ import annotations
from pydantic import BaseModel, Field, root_validator, validator
from typing import Any, Literal


class LLMProviderSettings(BaseModel):
    enabled: bool = False
    provider: str = "mock"
    model: str = "mock-v1"
    api_key: str | None = None
    timeout_seconds: int = 20
    max_tokens: int = 500

    @root_validator(pre=True)
    def load_from_env(cls, values: dict[str, Any]) -> dict[str, Any]:
        values.setdefault("enabled", cls._load_bool("LLM_ENABLED", False))
        values.setdefault("provider", cls._load_str("LLM_PROVIDER", "mock"))
        values.setdefault("model", cls._load_str("LLM_MODEL", "mock-v1"))
        values.setdefault("api_key", cls._load_str("LLM_API_KEY", None))
        values.setdefault("timeout_seconds", cls._load_int("LLM_TIMEOUT_SECONDS", 20))
        values.setdefault("max_tokens", cls._load_int("LLM_MAX_TOKENS", 500))
        return values

    @staticmethod
    def _load_str(name: str, default: Any) -> Any:
        return __import__("os").environ.get(name, default)

    @staticmethod
    def _load_int(name: str, default: int) -> int:
        value = __import__("os").environ.get(name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    @staticmethod
    def _load_bool(name: str, default: bool) -> bool:
        value = __import__("os").environ.get(name)
        if value is None:
            return default
        return value.lower() in {"1", "true", "yes", "on"}


class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int | None = None

    @validator("prompt")
    def prompt_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Prompt must not be empty")
        return value


class LLMResponse(BaseModel):
    provider: str
    model: str
    generated_text: str
    tokens_used: int
    max_tokens_requested: int | None = None


class LLMModelOutput(BaseModel):
    recommendation: str
    protected_fields: list[str] = Field(default_factory=list)
    risk_score: float
    recommendation_readable: str
    narrative: str
    protected_fields_changed: bool = False

    @validator("recommendation")
    def recommendation_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("recommendation cannot be empty")
        return value

    @validator("risk_score")
    def risk_score_must_be_in_range(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("risk_score must be between 0.0 and 1.0")
        return value

    @validator("protected_fields_changed")
    def protected_fields_must_remain_false(cls, value: bool) -> bool:
        if value is not False:
            raise ValueError("protected_fields_changed must be false")
        return value

    @validator("recommendation_readable", "narrative")
    def text_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text fields must not be empty")
        return value


class LLMMetadata(BaseModel):
    enabled: bool
    provider: str
    model: str
    validation: Literal["passed", "failed", "skipped", "not_executed"]
    fallback_used: bool
    latency_ms: int
    provider_executed: bool = False
    failure_reason: str | None = None
    validation_details: list[str] = Field(default_factory=list)


class LLMServiceResult(BaseModel):
    output: LLMModelOutput
    metadata: LLMMetadata
    validation_status: Literal["passed", "failed", "skipped"]
    fallback_used: bool
