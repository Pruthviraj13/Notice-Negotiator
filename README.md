# Notice Negotiator

Notice Negotiator now has:

- a FastAPI backend that scores notice-period negotiation strength
- a React frontend that collects company details and shows the plan visually

## Backend

Install Python packages and run the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

Install JavaScript packages and run the React app:

```bash
npm install
npm run dev
```

The Vite dev server proxies `/analyze` to `http://127.0.0.1:8000`, so keep the FastAPI server running while using the UI.

## API Example

`POST /analyze`

```json
{
  "company_type": "startup",
  "notice_period": 30,
  "offer_in_hand": true,
  "buyout_allowed": true,
  "project_critical": "low",
  "manager_type": "supportive"
}
```

```json
{
  "score": 100,
  "probability": "High",
  "strategies": [
    "Negotiate aggressively with a clear last working day.",
    "Use buyout or transition leverage if the company resists.",
    "Use your manager as an ally to shape a smoother exit plan.",
    "Keep buyout as a backup option during final negotiation."
  ]
}
```

## Learning Map

If you are new to React, start here:

1. [src/App.jsx](D:\PROJECTS\NoticeNegotiator\src\App.jsx) for component structure, state, and event handlers
2. [src/main.jsx](D:\PROJECTS\NoticeNegotiator\src\main.jsx) for how React mounts into the page
3. [src/styles.css](D:\PROJECTS\NoticeNegotiator\src\styles.css) for layout, colors, and responsive design
