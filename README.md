# Educational Debug Platform

A debugging practice platform for students. Users find and fix bugs in code, then submit their solution against hidden tests.

## Structure

```
├── backend/          ← FastAPI Python server (deploy to Railway)
│   ├── server.py
│   ├── requirements.txt
│   └── Procfile
├── frontend/         ← React/Vite app (deploy to Vercel)
│   ├── src/
│   ├── package.json
│   └── vercel.json
└── problems/         ← Problem files
    ├── Python/
    ├── TypeScript/
    └── CPP/
```

## Deployment

### Backend → Railway
1. Connect this repo to Railway
2. Set root directory to `backend`
3. Add environment variable: `PROBLEMS_DIR` = `/app/problems`
4. Copy problems folder to Railway using the extraFiles config

### Frontend → Vercel
1. Connect this repo to Vercel
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL` = your Railway backend URL

## Local Development

**Backend:**
```bash
cd backend
pip install fastapi uvicorn
python server.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
