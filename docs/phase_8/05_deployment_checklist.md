# Phase 8 Deployment Checklist

## Local Demo Setup

1. Confirm Docker Desktop is running.
2. From the repository root, start services:

```bash
docker compose up --build
```

3. Open the frontend:

```text
http://localhost:5173
```

4. Open the backend API docs:

```text
http://localhost:8000/docs
```

## Demo Preparation

- Seed data is defined in `backend/seed_data.py`.
- Recommended demo case: `CLM2001`.
- Run a case review from the dashboard before showing the queue if the queue is empty.
- Use Risk Queue and Case Detail for the main walkthrough.

## Validation Commands

Frontend:

```bash
cd frontend
npm run build
```

Backend:

```bash
cd backend
python -m compileall app
```

## Pre-Demo Checklist

- Dashboard loads.
- Risk Queue loads.
- Case Detail opens for `CLM2001`.
- Agent timeline displays after a case review has been run.
- Product boundary is stated clearly.
- Known limitations are available for review.
