from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

app = FastAPI(
    title="Where Is My Space API",
    description="Local prototype for estimating room occupancy from an image.",
    version="0.1.0",
)

# OpenCV's built-in HOG people detector is used only as a baseline demo.
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health():
    return {"status": "ok", "project": "Where Is My Space", "version": "0.1.0"}


@app.post("/api/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    capacity: int = Form(...),
):
    """Estimate visible people in an image. The image is not written to disk."""
    if capacity < 1 or capacity > 1000:
        raise HTTPException(status_code=400, detail="Capacity must be between 1 and 1000.")

    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Upload a JPG or PNG image.")

    raw = await image.read(MAX_IMAGE_BYTES + 1)
    if not raw:
        raise HTTPException(status_code=400, detail="The uploaded image is empty.")
    if len(raw) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")

    encoded = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="The file could not be decoded as an image.")

    # Resize very large images to keep this student demo responsive.
    height, width = frame.shape[:2]
    max_dimension = 1280
    scale = min(1.0, max_dimension / max(height, width))
    if scale < 1.0:
        frame = cv2.resize(frame, (int(width * scale), int(height * scale)))

    rectangles, _weights = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05,
    )

    detected_people = len(rectangles)
    available_seats = max(capacity - detected_people, 0)

    # The raw image is only held in memory during this request.
    return {
        "detected_people": detected_people,
        "capacity": capacity,
        "estimated_available_seats": available_seats,
        "estimated_occupied_seats": min(detected_people, capacity),
        "status": "estimate_only",
        "warning": (
            "Experimental HOG estimate. Seated or partially hidden people may be missed; "
            "objects may be misclassified. Verify manually."
        ),
    }


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
