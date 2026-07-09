from typing import Any


class PromptTemplates:
    @staticmethod
    def build_consolidator_prompt(context: dict[str, Any], instructions: str | None = None) -> str:
        base = [
            "You are an assistant that summarizes deterministic claim consolidation outputs.",
            "Do not modify any deterministic values. Do not invent facts. Use only the information provided.",
            "Produce structured JSON only.",
            "The JSON must include the following keys:",
            "- recommendation: a short decision string that matches deterministic values.",
            "- protected_fields: an array of sensitive fields that must remain unchanged.",
            "- risk_score: a numeric value between 0.0 and 1.0.",
            "- recommendation_readable: a clear human-friendly summary of the recommendation.",
            "- narrative: an explainable narrative that describes the decision.",
            "- protected_fields_changed: must always be false.",
        ]
        if instructions:
            base.append(instructions)

        base.append("Context:")
        base.append(str(context))
        base.append("Return JSON only with the exact keys listed above. Do not add extra explanation outside the JSON.")
        return "\n".join(base)
