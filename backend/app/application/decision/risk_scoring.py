class RiskScoringService:
    risk_weights = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

    def score(self, agent_outputs: list[dict]) -> dict:
        max_score = max([self.risk_weights.get(o.get("risk_level", "Low"), 1) for o in agent_outputs], default=1)
        risk_level = next(k for k, v in self.risk_weights.items() if v == max_score)
        return {
            "risk_level": risk_level,
            "score": max_score,
            "explainability_notes": self.explain(agent_outputs, risk_level, max_score),
        }

    def explain(self, agent_outputs: list[dict], risk_level: str, score: int) -> list[str]:
        notes = [f"Risk score {score} assigned from highest contributing risk level: {risk_level}."]
        for output in agent_outputs:
            agent_name = output.get("agent_name", "Unknown Agent")
            output_risk = output.get("risk_level", "Low")
            recommendation = output.get("recommendation", "No recommendation supplied.")
            notes.append(f"{agent_name} reported {output_risk} risk: {recommendation}")
        return notes
