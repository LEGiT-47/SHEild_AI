import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AnalyzeUploadSerializer
from .services import build_action_steps, call_fastapi, compute_risk
from .traceability import get_traceability

CASES_STORE = Path(settings.MEDIA_ROOT) / "cases.json"


def _load_cases() -> dict:
    if not CASES_STORE.exists():
        return {}
    try:
        return json.loads(CASES_STORE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_case(case_id: str, payload: dict) -> None:
    data = _load_cases()
    data[case_id] = payload
    CASES_STORE.parent.mkdir(parents=True, exist_ok=True)
    CASES_STORE.write_text(json.dumps(data, indent=2), encoding="utf-8")


class AnalyzeView(APIView):
    def post(self, request):
        serializer = AnalyzeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded = serializer.validated_data["file"]
        case_id = f"CASE-{str(uuid4())[:8].upper()}"
        extension = Path(uploaded.name).suffix or ".bin"
        unique_name = f"{uuid4()}{extension}"

        upload_dir = Path(settings.MEDIA_ROOT) / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / unique_name

        with file_path.open("wb+") as destination:
            for chunk in uploaded.chunks():
                destination.write(chunk)

        ai_result = call_fastapi(str(file_path))
        confidence = float(ai_result.get("confidence", 0.0))
        risk_level = compute_risk(confidence)
        action_steps = build_action_steps(risk_level)
        traceability = get_traceability(str(file_path))

        verdict = "DEEPFAKE" if ai_result.get("is_fake") else "AUTHENTIC"
        analyzed_at = datetime.now(timezone.utc).isoformat()

        response_data = {
            "case_id": case_id,
            "verdict": verdict,
            "is_fake": bool(ai_result.get("is_fake", False)),
            "confidence": confidence,
            "risk_level": risk_level,
            "artifacts": ai_result.get("artifacts", []),
            "traceability": traceability,
            "action_steps": action_steps,
            "file_url": f"{settings.MEDIA_URL}uploads/{unique_name}",
            "analyzed_at": analyzed_at,
            "face_detected": ai_result.get("face_detected", False),
            "blur_score": ai_result.get("blur_score", 0.0),
            "edge_anomaly_score": ai_result.get("edge_anomaly_score", 0.0),
        }

        _save_case(case_id, response_data)
        return Response(response_data, status=status.HTTP_200_OK)


class ReportView(APIView):
    def get(self, request, case_id: str):
        cases = _load_cases()
        case_data = cases.get(case_id)
        if not case_data:
            return Response({"detail": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(case_data, status=status.HTTP_200_OK)
