# SHEild AI - Deepfake Protection System

SHEild AI is a hackathon-ready forensic deepfake detection platform using a microservices architecture.

## Architecture

- Frontend: React + Vite + Tailwind + Framer Motion
- Backend: Django REST Framework
- AI Service: FastAPI + OpenCV

## Prerequisites

- Node.js 18+
- Python 3.10+
- pip

## FastAPI Setup (AI Service)

```bash
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Health check:

```bash
GET http://localhost:8001/health
```

## Django Setup (Main Backend)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Main API base: `http://localhost:8000/api/`

## Real Traceability API Setup (Optional)

By default, traceability runs in `mock` mode. To use real reverse-image search:

1. Create accounts and get API credentials:
- SerpAPI: https://serpapi.com/ (Google Lens search)
- Cloudinary: https://cloudinary.com/ (host uploaded image so Lens can access URL)

2. Configure `backend/.env`:

```env
TRACEABILITY_PROVIDER=serpapi
SERPAPI_API_KEY=your_serpapi_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```

3. Restart Django server.

If keys are missing or API fails, the app automatically falls back to mock traceability so demo flow still works.

## React Setup (Frontend)

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Demo Flow

1. Open frontend and click `OPEN CASE FILE`
2. Upload an image (or short video)
3. Click `ANALYZE`
4. Review verdict, risk level, evidence artifacts, traceability board, action steps
5. Generate legal complaint text and copy it

## Endpoint Summary

### Django API

- `POST /api/analyze/`
- `GET /api/report/{case_id}/`
- `POST /api/report/generate/`

### FastAPI API

- `POST /detect/`
- `GET /health`

## Screenshot Placeholders

- docs/home.png
- docs/upload.png
- docs/result.png
