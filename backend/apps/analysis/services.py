from pathlib import Path

import httpx
from django.conf import settings


class FastAPIServiceError(Exception):
    pass


def call_fastapi(file_path: str) -> dict:
    detect_url = f"{settings.FASTAPI_URL}/detect/"
    path = Path(file_path)
    with path.open("rb") as f:
        files = {"file": (path.name, f, "application/octet-stream")}
        try:
            response = httpx.post(detect_url, files=files, timeout=20.0)
        except httpx.RequestError as exc:
            raise FastAPIServiceError(f"Could not reach AI service at {detect_url}") from exc

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        body_preview = (exc.response.text or "")[:200]
        raise FastAPIServiceError(
            f"AI service returned {exc.response.status_code}: {body_preview}"
        ) from exc

    try:
        return response.json()
    except ValueError as exc:
        raise FastAPIServiceError("AI service returned invalid JSON") from exc


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
