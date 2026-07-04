class RiskScoringService:
    risk_weights = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

    def score(self, agent_outputs: list[dict]) -> dict:
        max_score = max([self.risk_weights.get(o.get("risk_level", "Low"), 1) for o in agent_outputs], default=1)
        risk_level = next(k for k, v in self.risk_weights.items() if v == max_score)
        return {"risk_level": risk_level, "score": max_score}
