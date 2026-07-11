Summary of actions performed

- Seeded demo data into a local SQLite DB: `backend/ahip_demo.db` using the updated `backend/seed_data.py` script.
- Started the backend API (FastAPI) with `PYTHONPATH=backend` and `DATABASE_URL=sqlite:///backend/ahip_demo.db`.
- Started the frontend dev server (Vite) and built a production bundle.
- Verified API endpoints and integration:
  - GET `/api/v1/dashboard/summary` returned consistent metrics.
  - GET `/api/v1/agents/priority-queue` returned 3 recommendations (CLM2002, CLM2001, CLM2005).
  - Case review run endpoint `/api/v1/agents/run-case-review` works and populates shared memory and agent executions.
- Ran backend unit tests (17 passed).
- Fixed an orchestrator bug to ensure demo default contexts are used when DB records are absent and corrected provider contract context wiring. This fixed a failing test.

Commands used (copy/paste):

```powershell
# Seed DB (SQLite)
$env:DATABASE_URL='sqlite:///backend/ahip_demo.db'; python backend/seed_data.py

# Start backend (development)
$env:PYTHONPATH='backend'; $env:DATABASE_URL='sqlite:///backend/ahip_demo.db'; python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Start frontend dev server
npm run dev --prefix frontend

# Build frontend
npm run build --prefix frontend

# Run backend tests
$env:PYTHONPATH='backend'; python -m pytest -q
```

Notes and next steps

- Frontend search, filters, and buttons were inspected and are wired to the backend API; the `RiskQueueView` and `CaseDetailView` are functional with the seeded demo data.
- If you want, I can:
  - Commit the orchestrator fix and open a PR.
  - Add a lightweight smoke test that starts the backend and verifies critical endpoints.
  - Create a short demo script to run frontend + backend and open the browser automatically.
