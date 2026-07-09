import json
from time import perf_counter
from typing import Any

from app.application.graphs.workflow_state import WorkflowState
from .provider_adapter import get_provider
from .prompt_templates import PromptTemplates
from .schemas import (
    LLMMetadata,
    LLMModelOutput,
    LLMProviderSettings,
    LLMRequest,
    LLMResponse,
    LLMServiceResult,
)
from .validators import parse_and_validate_model_output, validate_json_schema


class LLMService:
    def __init__(self, settings: LLMProviderSettings | None = None) -> None:
        self.settings = settings or LLMProviderSettings()
        self.provider_error: str | None = None
        try:
            self.provider = get_provider(self.settings)
        except Exception as exc:
            self.provider = None
            self.provider_error = str(exc)

    def _sanitize_value(self, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, dict):
            return {
                str(key): self._sanitize_value(val)
                for key, val in value.items()
                if isinstance(key, (str, int, float, bool))
            }
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        return None

    def _build_safe_context(self, state: WorkflowState) -> dict[str, Any]:
        shared_memory = state.shared_context.get("shared_memory") if isinstance(state.shared_context, dict) else None
        safe_agent_outputs = [
            self._sanitize_value(output)
            for output in state.agent_outputs
            if isinstance(output, dict)
        ]

        recommendations = []
        if isinstance(state.recommendation, dict):
            recommendations.append(self._sanitize_value(state.recommendation))

        risk_levels = []
        for output in state.agent_outputs:
            if isinstance(output, dict):
                for key in ("risk_score", "risk_level", "risk"):
                    if key in output:
                        value = output.get(key)
                        if isinstance(value, (int, float)):
                            risk_levels.append(value)
        if isinstance(state.recommendation, dict) and "risk_score" in state.recommendation:
            value = state.recommendation.get("risk_score")
            if isinstance(value, (int, float)):
                risk_levels.append(value)

        return {
            "case_id": state.case_id,
            "selected_route": state.selected_route,
            "agent_outputs": safe_agent_outputs,
            "shared_memory": self._sanitize_value(shared_memory) if shared_memory is not None else {},
            "recommendations": recommendations,
            "risk_levels": risk_levels,
        }

    def _build_fallback_output(self) -> LLMModelOutput:
        return LLMModelOutput(
            recommendation="defer",
            protected_fields=[],
            risk_score=0.0,
            recommendation_readable="Deterministic fallback recommendation applied.",
            narrative="The LLM service could not produce a valid structured response, so a deterministic fallback was used.",
            protected_fields_changed=False,
        )

    def _build_metadata(
        self,
        validation: str,
        fallback_used: bool,
        latency_ms: int,
        provider_executed: bool = False,
        failure_reason: str | None = None,
        validation_details: list[str] | None = None,
    ) -> LLMMetadata:
        return LLMMetadata(
            enabled=self.settings.enabled,
            provider=self.settings.provider,
            model=self.settings.model,
            validation=validation,
            fallback_used=fallback_used,
            latency_ms=latency_ms,
            provider_executed=provider_executed,
            failure_reason=failure_reason,
            validation_details=validation_details or [],
        )

    def generate_from_state(
        self,
        state: WorkflowState,
        instructions: str | None = None,
    ) -> LLMServiceResult:
        safe_context = self._build_safe_context(state)
        prompt = PromptTemplates.build_consolidator_prompt(safe_context, instructions=instructions)
        request = LLMRequest(prompt=prompt, max_tokens=self.settings.max_tokens)

        start = perf_counter()
        validation_status = "skipped"
        fallback_used = False
        validation_details: list[str] = []
        output = self._build_fallback_output()

        if not self.settings.enabled:
            elapsed_ms = int((perf_counter() - start) * 1000)
            metadata = self._build_metadata(
                "not_executed",
                False,
                elapsed_ms,
                provider_executed=False,
            )
            return LLMServiceResult(
                output=self._build_fallback_output(),
                metadata=metadata,
                validation_status="skipped",
                fallback_used=False,
            )

        if self.provider_error is not None:
            elapsed_ms = int((perf_counter() - start) * 1000)
            metadata = self._build_metadata(
                "failed",
                True,
                elapsed_ms,
                provider_executed=False,
                failure_reason=self.provider_error,
                validation_details=[self.provider_error],
            )
            return LLMServiceResult(
                output=self._build_fallback_output(),
                metadata=metadata,
                validation_status="failed",
                fallback_used=True,
            )

        try:
            response_data = self.provider.generate(request.prompt, max_tokens=request.max_tokens)
            elapsed_ms = int((perf_counter() - start) * 1000)
            metadata = self._build_metadata("skipped", False, elapsed_ms, provider_executed=True)

            provider_response = LLMResponse.parse_obj(response_data)
            is_valid, errors, payload = parse_and_validate_model_output(provider_response.generated_text)
            if not is_valid or payload is None:
                validation_status = "failed"
                fallback_used = True
                validation_details = errors
                metadata = self._build_metadata(
                    validation_status,
                    fallback_used,
                    elapsed_ms,
                    provider_executed=True,
                    failure_reason=errors[0] if errors else "Validation failed",
                    validation_details=validation_details,
                )
                output = self._build_fallback_output()
            else:
                output = LLMModelOutput.parse_obj(payload)
                validation_status = "passed"
                metadata = self._build_metadata(
                    validation_status,
                    False,
                    elapsed_ms,
                    provider_executed=True,
                )
        except Exception as exc:
            elapsed_ms = int((perf_counter() - start) * 1000)
            validation_status = "failed"
            fallback_used = True
            validation_details = [str(exc)]
            metadata = self._build_metadata(
                validation_status,
                fallback_used,
                elapsed_ms,
                provider_executed=True,
                failure_reason=str(exc),
                validation_details=validation_details,
            )
            output = self._build_fallback_output()

        return LLMServiceResult(
            output=output,
            metadata=metadata,
            validation_status=validation_status,
            fallback_used=fallback_used,
        )

    def generate(self, request: LLMRequest) -> tuple[LLMResponse, LLMMetadata]:
        start = perf_counter()
        response_data = self.provider.generate(request.prompt, max_tokens=request.max_tokens or self.settings.max_tokens)
        latency_ms = int((perf_counter() - start) * 1000)
        response = LLMResponse.parse_obj(response_data)
        metadata = self._build_metadata("skipped", False, latency_ms)
        return response, metadata
