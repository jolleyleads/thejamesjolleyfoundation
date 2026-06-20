# The James Jolley Foundation DOE Command Center

Turning Losses Into Lifelines.

This is a backend-powered charity website using the DOE Framework.

Routes:
- /
- /health
- /api/intake
- /api/outreach

Render:
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
