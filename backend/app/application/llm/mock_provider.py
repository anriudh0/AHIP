import json

from .provider_adapter import LLMProvider


class MockProvider(LLMProvider):
    def generate(self, prompt: str, max_tokens: int | None = None) -> dict:
        payload = {
            "recommendation": "approve",
            "protected_fields": ["patient_name", "member_id"],
            "risk_score": 0.12,
            "recommendation_readable": "Approve the claim with low risk and preserve protected patient identifiers.",
            "narrative": "Based on the deterministic outputs, this claim meets approval criteria without altering protected fields.",
            "protected_fields_changed": False,
        }
        return {
            "provider": "mock",
            "model": "mock-v1",
            "generated_text": json.dumps(payload),
            "tokens_used": 42,
            "max_tokens_requested": max_tokens,
        }
