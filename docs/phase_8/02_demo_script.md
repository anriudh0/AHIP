# Phase 8 Demo Script

Target duration: 10 minutes.

## 1. Position AHIP

AHIP is a healthcare operations intelligence platform for surfacing claims, provider, compliance, and patient-journey workflow gaps. It is not a chatbot, not a generic RAG app, and not a diagnosis tool.

## 2. Start The Product

```bash
docker compose up --build
```

Open the frontend at:

```text
http://localhost:5173
```

## 3. Show Executive Dashboard

Open the dashboard and explain:

- Open operational cases
- High-risk members
- Claim exceptions
- Contract issues
- Compliance gaps
- Governance summary

## 4. Run A Case Review

Use the dashboard workflow action with:

```text
CLM2001
```

Explain that AHIP runs deterministic agents, stores execution history, and produces a consolidated recommendation.

## 5. Open Risk Queue

Navigate to Risk Queue and show:

- Risk level
- Numeric score
- Priority
- Escalation owner
- Recommendation
- Filters by case, risk, priority, and status

## 6. Open Case Detail

Click `CLM2001` and show:

- Consolidated recommendation
- Evidence and explainability notes
- Claim context pack
- Patient journey context pack
- Compliance context pack
- Relationship mapping
- Agent execution timeline

## 7. Close With Product Value

AHIP helps operations teams identify why a case needs attention, who should own it, and what evidence supports the recommendation. Human review remains part of the workflow.
