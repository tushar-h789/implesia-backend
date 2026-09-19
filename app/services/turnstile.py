import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_turnstile(token: str | None, remote_ip: str | None = None) -> bool:
    """Validate a Cloudflare Turnstile token. Returns True when checks are disabled."""
    if not settings.turnstile_enabled:
        return True
    if not token:
        return False

    payload = {"secret": settings.turnstile_secret_key, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(VERIFY_URL, data=payload)
            response.raise_for_status()
            return bool(response.json().get("success"))
    except httpx.HTTPError as exc:
        logger.error("turnstile_unreachable", error=str(exc))
        # Fail closed: an unverifiable submission is treated as a failure.
        return False
