# Web interface

React + Vite + MUI front end for the rule-based detector API (`technique1/app.py`).

```bash
npm install
npm run dev      # http://localhost:3000 (expects the API on http://127.0.0.1:5000)
npm test         # unit tests (Vitest + Testing Library)
npm run build    # production build in dist/
```

Set `VITE_API_URL` to point the UI at another API address.
