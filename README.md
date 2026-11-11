# Where Is My Space

**Physical space, understood.**

Where Is My Space is an early-stage, privacy-conscious prototype for estimating occupancy in shared spaces such as college libraries and study rooms. The first milestone is a small local demo: select or capture a room image, estimate the number of visible people, and calculate the number of potentially available seats from a user-entered room capacity.

> **Prototype limitation:** The included OpenCV HOG detector is a baseline demonstration, not a reliable production occupancy system. It can miss people, count incorrectly, and perform poorly with seated, partially hidden, or distant people. Do not use its output for safety-critical decisions or official capacity enforcement.

## Current features

- Local FastAPI backend.
- Simple browser interface.
- Image upload and optional camera capture (browser permission required).
- OpenCV HOG-based person detection.
- Estimated occupied and available seats based on a manually entered capacity.
- Images are processed in memory and are not saved by the application.

## Project structure

```text
Where-Is-My-Space/
├── backend/
│   ├── __init__.py
│   └── app.py
├── docs/
│   ├── project-overview.md
│   └── privacy.md
├── frontend/
│   └── index.html
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Git
- GitHub Desktop
- A modern browser

## Run locally (Windows PowerShell)

Open PowerShell in the project folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

If PowerShell blocks activation, run this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open **http://127.0.0.1:8000** in your browser.

API health check: http://127.0.0.1:8000/api/health

Interactive API documentation: http://127.0.0.1:8000/docs

## How to test

1. Start the server using the commands above.
2. Open the local website.
3. Enter the room's total seat capacity.
4. Upload a room image, or use **Open camera** and then **Capture photo**.
5. Select **Analyze occupancy**.
6. Review the estimated count and available-seat estimate.

Use a test image that you have permission to process. For the first demo, avoid images containing identifiable people unless you have their consent.

## Important privacy note

This prototype processes the selected image on the same computer where the server is running. It does not intentionally save or transmit the image to a third-party service. The browser sends the image to your local backend at `127.0.0.1`. Read [docs/privacy.md](docs/privacy.md) before testing with real people.

## Roadmap

- [x] Create initial public project structure.
- [x] Build a local web interface and API prototype.
- [x] Add a baseline computer-vision detector.
- [ ] Test with consented sample images in the target room.
- [ ] Measure false positives and false negatives.
- [ ] Explore a more suitable model for seated-person detection.
- [ ] Add manual correction and confidence/limitations messaging.
- [ ] Evaluate sensor-assisted occupancy estimation.
- [ ] Deploy only after privacy, security, and accuracy reviews.

## Contributing

This is an early-stage student project. Issues, documented test results, and focused pull requests are welcome. Do not commit private CCTV footage, identifiable images, API keys, passwords, or other sensitive data.

## License

Released under the MIT License. See [LICENSE](LICENSE).
