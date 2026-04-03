# SHEild AI - Hackathon Documentation Guide

## 1. Elevator Pitch

SHEild AI is a privacy-first, microservice-based deepfake response platform built for real-time citizen protection. It combines forensic media analysis, source traceability, legal-ready reporting, and action guidance into a single workflow so users can move from suspicion to evidence-backed response in minutes.

## 2. Problem Statement

Deepfake and manipulated media are increasingly used for:

- Harassment and extortion
- Non-consensual image misuse
- Reputation damage
- Social misinformation

Most users lack tools that are:

- Simple enough for non-technical users
- Fast enough for urgent incidents
- Actionable beyond a binary fake/authentic label

## 3. Solution Overview

SHEild AI addresses this with three integrated layers:

- Detection Layer: analyzes media for visual inconsistencies and outputs confidence and risk level
- Traceability Layer: checks whether similar media appears elsewhere (mock or live provider)
- Response Layer: gives legal-aware action steps and complaint text generation support

## 4. What We Built

### Frontend (User Experience)

- React + Vite application for fast upload and result flow
- Guided case flow from upload to decision support
- Visual risk meter and evidence artifacts
- Traceability board and action panel for immediate next steps

### Backend (Case Orchestration)

- Django REST API for upload handling, orchestration, and reporting
- Calls AI microservice for media scoring
- Stores case analysis payloads for report retrieval
- Provides report-generation endpoint for legal/escalation workflow

### AI Service (Forensic Engine)

- FastAPI service with OpenCV/Numpy forensic pipeline
- Combines multiple visual indicators into a confidence score
- Returns explainable artifacts (not just raw score)

## 5. Core Tech Stack

### Frontend

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios

### Backend

- Django
- Django REST Framework
- django-cors-headers
- httpx
- gunicorn

### AI Service

- FastAPI
- Uvicorn
- OpenCV (opencv-python-headless)
- NumPy

### Infrastructure

- Render for backend and AI web services
- Netlify for frontend hosting
- Optional Netlify scheduled keep-alive caller

## 6. How Detection Works (Implementation)

The AI service uses a heuristic forensic scoring pipeline:

1. Decode and normalize image input
2. Face presence check (Haar cascade; fallback behavior if unavailable)
3. Blur analysis via Laplacian variance
4. Edge anomaly analysis with Canny-based density comparison
5. Compression artifact signal (8x8 blockiness estimation)
6. Lighting inconsistency signal (gradient direction distribution)
7. Weighted signal fusion into final confidence in [0, 1]

Output includes:

- `is_fake`
- `confidence`
- `artifacts` list explaining suspicious signals
- `face_detected`, `blur_score`, `edge_anomaly_score`

## 7. Is ML Used?

Yes, in the broad applied-AI/computer-vision sense, but not as a trained deep neural model.

Current model type:

- Rule-based forensic CV pipeline using OpenCV + handcrafted features and weighted decision logic

What this means:

- Strong explainability for hackathon demos
- No dataset-trained benchmark claim yet
- Accuracy cannot be honestly reported as a fixed percentage without labeled evaluation

## 8. Why SHEild Stands Out (Hackathon Differentiators)

Compared to many detector-only demos, SHEild AI is stronger on end-to-end utility:

- Actionability: turns detection into concrete response steps
- Explainability: surfaces artifact-level evidence, not black-box output
- Traceability integration: checks external propagation signals
- Legal readiness: complaint/report workflow in-product
- Deployment-ready architecture: separated frontend, API, and AI service for scale

## 9. Judging-Criteria Mapping

### Innovation

- Combines forensic analysis + traceability + legal-action support in one user flow

### Technical Depth

- Microservices architecture with cross-service orchestration
- Multi-signal CV analysis instead of single-threshold logic
- API-first design for modular extensibility

### Impact

- Addresses abuse scenarios that affect vulnerable users
- Supports faster escalation with structured evidence and guidance

### Feasibility

- Deployable on common startup-friendly cloud stack (Render + Netlify)
- Works in mock traceability mode if external APIs are unavailable

### UX

- Clear case-based journey from upload to recommendation
- Human-readable verdict and risk communication

## 10. Security and Privacy Notes

- Do not commit secrets to source control
- Keep API keys in platform environment variables
- Rotate exposed credentials immediately
- Add file-size/type limits and malware scanning in production hardening phase

## 11. Deployment Snapshot

### Backend + AI (Render)

- Two independent web services:
  - `sheild-backend`
  - `sheild-ai-service`

### Frontend (Netlify)

- Vite build output served from `frontend/dist`
- `VITE_API_BASE_URL` points to backend service

## 12. Known Limits (Honest Statement)

- No formal benchmark accuracy published yet
- Current persistence is lightweight; production should use managed database/object storage
- Traceability quality depends on external provider availability and API quotas

## 13. Next Milestones

- Build labeled evaluation set and publish precision/recall/F1
- Add video-native temporal inconsistency checks
- Add user authentication and secure case ownership
- Add audit trail for evidentiary chain-of-custody

## 14. Demo Script (2-3 Minutes)

1. Upload suspicious media
2. Trigger analysis and show confidence/risk
3. Explain artifact evidence in plain language
4. Open traceability panel to show source checks
5. Generate complaint/report output and summarize action steps

## 15. One-Line Positioning

SHEild AI is not just a deepfake detector; it is a practical incident-response system for manipulated media.
