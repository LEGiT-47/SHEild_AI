from pathlib import Path

import httpx
from django.conf import settings


def call_fastapi(file_path: str) -> dict:
    detect_url = f"{settings.FASTAPI_URL}/detect/"
    path = Path(file_path)
    with path.open("rb") as f:
        files = {"file": (path.name, f, "application/octet-stream")}
        response = httpx.post(detect_url, files=files, timeout=20.0)
    response.raise_for_status()
    return response.json()


def compute_risk(confidence: float) -> str:
    if confidence >= 0.75:
        return "HIGH"
    if confidence >= 0.45:
        return "MEDIUM"
    return "LOW"


def build_action_steps(risk_level: str) -> list[str]:
    if risk_level == "HIGH":
        return [
            "Preserve original file and avoid editing or forwarding.",
            "File a cybercrime complaint immediately with this case report.",
            "Contact platform abuse and safety team with case evidence.",
            "Consult legal support under IT Act Sections 66E and 67.",
        ]
    if risk_level == "MEDIUM":
        return [
            "Document each occurrence with timestamped screenshots.",
            "Monitor platform activity for reposts or mirrors.",
            "Notify a trusted contact and share the case reference.",
            "Collect account/profile links for escalation.",
        ]
    return [
        "File appears likely authentic with minor inconsistencies.",
        "Monitor future distribution for suspicious edits.",
        "Keep an original copy of this media for records.",
    ]
