# Privacy and data handling

This is a local educational prototype, not a deployed surveillance system.

- The browser sends the selected image to the FastAPI server running at `127.0.0.1`.
- The API decodes and analyzes the image in memory.
- The application does not intentionally write uploaded images to disk.
- The prototype does not use face recognition, identity matching, or person tracking.
- Camera access is optional and requires explicit browser permission.
- Camera use stops when the page is closed.

## Before any real-world test

1. Obtain permission from the facility owner and informed consent where required.
2. Prefer staged test images without identifiable people.
3. Do not connect institutional CCTV without written authorization.
4. Do not commit test images, video, credentials, or personal data to GitHub.
5. Review applicable institutional rules and privacy requirements before deployment.

Local processing does not by itself guarantee privacy. The device, browser, server, and operating system still need to be secured.
