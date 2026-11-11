from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

app = FastAPI(
    title="Where Is My Space API",
    description="Privacy-conscious room occupancy prototype.",
    version="0.2.0",
)

# YOLO person detector
person_model = YOLO("yolov8n.pt")

# OpenCV face detector (no face identity recognition)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "project": "Where Is My Space",
        "version": "0.2.0"
    }


@app.post("/api/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    capacity: int = Form(...)
):
    if capacity < 1 or capacity > 1000:
        raise HTTPException(status_code=400, detail="Invalid capacity.")

    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Upload JPG or PNG.")

    raw = await image.read(MAX_IMAGE_BYTES + 1)

    if not raw:
        raise HTTPException(status_code=400, detail="Empty image.")

    if len(raw) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image too large.")

    frame = cv2.imdecode(
        np.frombuffer(raw, dtype=np.uint8),
        cv2.IMREAD_COLOR
    )

    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image.")

    height, width = frame.shape[:2]
    scale = min(1.0, 1280 / max(height, width))

    if scale < 1.0:
        frame = cv2.resize(
            frame,
            (int(width * scale), int(height * scale))
        )

    # YOLO person detection
    results = person_model.predict(
        frame,
        imgsz=640,
        conf=0.35,
        classes=[0],
        device="cpu",
        verbose=False
    )

    person_count = len(results[0].boxes) if results[0].boxes is not None else 0

    # Face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    face_count = len(faces)

    # Use the higher count as an experimental estimate.
    detected_people = max(person_count, face_count)

    available_seats = max(capacity - detected_people, 0)

    return {
        "detected_people": detected_people,
        "detected_faces": face_count,
        "detected_person_bodies": person_count,
        "capacity": capacity,
        "estimated_available_seats": available_seats,
        "estimated_occupied_seats": min(detected_people, capacity),
        "status": "estimate_only",
        "warning": (
            "Experimental face and person detection. "
            "Hidden faces, side views, overlapping people and "
            "false detections can affect accuracy. "
            "This is not yet verified seat-level occupancy."
        )
    }


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)