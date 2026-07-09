import json
from typing import Any
from pydantic import BaseModel, ValidationError
from .schemas import LLMModelOutput


def validate_json_schema(data: Any, schema: type[BaseModel]) -> tuple[bool, list[str]]:
    try:
        schema.parse_obj(data)
        return True, []
    except ValidationError as exc:
        return False, [err["msg"] for err in exc.errors()]


def parse_and_validate_model_output(text: str) -> tuple[bool, list[str], dict[str, Any] | None]:
    if not text or not text.strip():
        return False, ["Empty model output"], None

    if len(text) > 10000:
        return False, ["Model output exceeds maximum allowed length"], None

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return False, [f"Invalid JSON: {exc.msg}"], None

    is_valid, errors = validate_json_schema(payload, LLMModelOutput)
    if not is_valid:
        return False, errors, None

    return True, [], payload
