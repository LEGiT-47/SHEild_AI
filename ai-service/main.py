from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from models.detector import DeepfakeDetector

app = FastAPI(title="SHEild AI Service")
detector = DeepfakeDetector()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model": "opencv-v1"}


@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detector.analyze(image_bytes)
    return result
