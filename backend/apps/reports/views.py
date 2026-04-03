from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ComplaintGeneratorView(APIView):
    def post(self, request):
        case_id = request.data.get("case_id")
        verdict = request.data.get("verdict", "UNKNOWN")
        risk_level = request.data.get("risk_level", "MEDIUM")
        artifacts = request.data.get("artifacts", [])
        victim_name = request.data.get("victim_name", "[Victim Name]")
        platform = request.data.get("platform", "[Platform Name]")

        if not case_id:
            return Response(
                {"detail": "case_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        artifacts_text = "\n".join([f"- {item}" for item in artifacts]) or "- No major artifacts listed"

        complaint_text = f"""TO,
The Commissioner of Police,
Cyber Crime Cell

SUBJECT: Formal Complaint Regarding Deepfake / Morphed Media Abuse (Case ID: {case_id})

Respected Sir/Madam,

I, {victim_name}, wish to formally report a case of suspected image-based abuse identified through forensic analysis.

Case Summary:
- Case ID: {case_id}
- Platform Observed: {platform}
- Forensic Verdict: {verdict}
- Risk Level: {risk_level}

Detected Forensic Artifacts:
{artifacts_text}

Applicable Legal Provisions:
- Information Technology Act, 2000: Sections 66E, 67, 67A
- Indian Penal Code: Section 509

I request your office to kindly register this complaint, initiate a technical investigation, and direct the concerned platform(s) to remove harmful content and preserve evidence records.

I am prepared to provide all supporting material and cooperate with the investigation.

Sincerely,
{victim_name}
Date: __________________
Contact: __________________
"""

        return Response({"complaint_text": complaint_text}, status=status.HTTP_200_OK)
