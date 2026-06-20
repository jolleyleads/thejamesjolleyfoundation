# The James Jolley Foundation DOE Command Center

Turning Losses Into Lifelines

This is a backend-powered nonprofit website, not a static flyer.

## Routes

- `/` public website
- `/health` system check
- `/api/intake` donation, help, partner, volunteer, and media intake
- `/api/outreach` Outreach Monster endpoint

## DOE Framework

### D — Directives
Save lives, accept donations, capture urgent help requests, and build support.

### O — Orchestration
Route each submission by category and urgency.

### E — Execution
Notify admin, send to Make.com, prepare AI summaries, and create follow-up actions.

## Render Settings

Build Command:

`pip install -r requirements.txt`

Start Command:

`gunicorn app:app`

Root Directory:

`.`

## Environment Variables

- `ADMIN_EMAIL`
- `MAKE_WEBHOOK_URL`
- `OPENAI_API_KEY`
