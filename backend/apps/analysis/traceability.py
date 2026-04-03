import hashlib
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import uniform
from urllib.parse import urlparse

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


def _source_from_url(target_url: str) -> str:
    hostname = (urlparse(target_url).hostname or "").lower()
    if "instagram.com" in hostname:
        return "Instagram"
    if "x.com" in hostname or "twitter.com" in hostname:
        return "Twitter/X"
    if "t.me" in hostname or "telegram" in hostname:
        return "Telegram"
    if "facebook.com" in hostname:
        return "Facebook"
    if "youtube.com" in hostname or "youtu.be" in hostname:
        return "YouTube"
    if "reddit.com" in hostname:
        return "Reddit"
    return hostname.replace("www.", "").split(".")[0].title() or "Unknown"


def _mock_traceability() -> list[dict]:
    now = datetime.now(timezone.utc).date()
    return [
        {
            "source": "Instagram",
            "url": "https://instagram.com/p/mock-trace-1",
            "found_at": str(now - timedelta(days=7)),
            "confidence": round(uniform(0.78, 0.95), 2),
        },
        {
            "source": "Twitter/X",
            "url": "https://x.com/user/status/mock-trace-2",
            "found_at": str(now - timedelta(days=5)),
            "confidence": round(uniform(0.65, 0.89), 2),
        },
        {
            "source": "Telegram",
            "url": "https://t.me/mock_channel/102",
            "found_at": str(now - timedelta(days=3)),
            "confidence": round(uniform(0.55, 0.84), 2),
        },
    ]


def _upload_to_cloudinary(file_path: str) -> str:
    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "")
    api_key = getattr(settings, "CLOUDINARY_API_KEY", "")
    api_secret = getattr(settings, "CLOUDINARY_API_SECRET", "")

    if not cloud_name or not api_key or not api_secret:
        raise RuntimeError("Cloudinary credentials are not configured")

    path = Path(file_path)
    timestamp = int(datetime.now(timezone.utc).timestamp())

    # Cloudinary signed upload requires SHA1 of params + API secret.
    signature_base = f"timestamp={timestamp}{api_secret}"
    signature = hashlib.sha1(signature_base.encode("utf-8")).hexdigest()

    # Use auto upload so both images and short videos are accepted.
    endpoint = f"https://api.cloudinary.com/v1_1/{cloud_name}/auto/upload"
    with path.open("rb") as f:
        files = {"file": (path.name, f, "application/octet-stream")}
        data = {
            "api_key": api_key,
            "timestamp": str(timestamp),
            "signature": signature,
        }
        response = httpx.post(endpoint, data=data, files=files, timeout=45.0)

    if response.status_code >= 400:
        raise RuntimeError(f"Cloudinary upload failed: {response.text}")
    payload = response.json()
    secure_url = payload.get("secure_url")
    if not secure_url:
        raise RuntimeError("Cloudinary upload did not return secure_url")
    return secure_url


def _search_with_serpapi(image_url: str) -> list[dict]:
    api_key = getattr(settings, "SERPAPI_API_KEY", "")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY is not configured")

    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": api_key,
    }
    response = httpx.get("https://serpapi.com/search.json", params=params, timeout=45.0)
    if response.status_code >= 400:
        raise RuntimeError(f"SerpAPI request failed: {response.text}")
    payload = response.json()

    matches = payload.get("visual_matches", []) or payload.get("exact_matches", [])
    today = str(datetime.now(timezone.utc).date())
    results: list[dict] = []

    for item in matches[:5]:
        link = item.get("link") or item.get("url")
        if not link:
            continue

        score = item.get("similarity") or item.get("score")
        if isinstance(score, (int, float)):
            confidence = float(score)
            if confidence > 1.0:
                confidence = confidence / 100.0
        else:
            confidence = 0.65

        results.append(
            {
                "source": _source_from_url(link),
                "url": link,
                "found_at": today,
                "confidence": round(max(0.0, min(confidence, 1.0)), 2),
            }
        )

    return results


def get_traceability(file_path: str) -> list[dict]:
    provider = getattr(settings, "TRACEABILITY_PROVIDER", "mock").lower()
    fallback_to_mock = getattr(settings, "TRACEABILITY_FALLBACK_TO_MOCK", True)

    if provider != "serpapi":
        return _mock_traceability()

    try:
        image_url = _upload_to_cloudinary(file_path)
        matches = _search_with_serpapi(image_url)
        if matches:
            return matches
        logger.warning("SerpAPI returned no visual matches for file: %s", file_path)
        if not fallback_to_mock:
            return []
    except Exception:
        logger.exception("Traceability provider failed for file: %s", file_path)
        if not fallback_to_mock:
            return []

    return _mock_traceability()
