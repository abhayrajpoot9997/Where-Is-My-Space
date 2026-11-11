# Project overview

## Problem

People entering shared facilities such as libraries and study rooms may not know which areas or seats are available. This can waste time and lead to inefficient use of existing space.

## Proposed direction

Where Is My Space aims to provide an occupancy estimate for a selected shared space. The initial proof of concept focuses on one room and a manually supplied seat capacity.

## Initial prototype

1. A user provides a room image using upload or a local camera.
2. The local Python API analyzes the image using a baseline OpenCV people detector.
3. The interface displays the detected-person count and a rough available-seat estimate.

## Assumptions to test

- A room image can provide useful occupancy information.
- A simple detector can be a useful first demonstration, even though its accuracy is limited.
- Users need an estimate, timestamp, and clear confidence/limitations messaging.
- Processing locally can reduce unnecessary transfer of image data.

## Validation plan

- Test only with consented or staged images.
- Include empty, partly occupied, crowded, seated, and partially occluded scenes.
- Manually label the actual number of people in each test image.
- Record false positives and false negatives.
- Do not claim accuracy until a representative test set has been evaluated.

## Out of scope for v0.1

- Production-grade accuracy.
- Continuous CCTV monitoring.
- Face recognition or identity tracking.
- Cloud image storage.
- Automatic room access or safety enforcement.
