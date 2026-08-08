import base64
import hashlib
import hmac
import os
import secrets
import time

import requests


BASE_URL = os.getenv(
    "ROUTESTACK_BASE_URL",
    "https://evolvemcp.routestack.ai",
)


def get_access_token():
    api_key = os.getenv("ROUTESTACK_API_KEY")
    api_secret = os.getenv("ROUTESTACK_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("RouteStack API credentials are missing")

    timestamp = int(time.time())
    nonce = secrets.token_urlsafe(24)

    message = f"{api_key}:{timestamp}:{nonce}"

    signature = hmac.new(
        api_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    signature = (
        base64.urlsafe_b64encode(signature)
        .decode("utf-8")
        .rstrip("=")
    )

    response = requests.post(
        f"{BASE_URL}/mcp/auth/partner-token",
        json={
            "apiKey": api_key,
            "timestamp": timestamp,
            "nonce": nonce,
            "hmac": signature,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "token" not in data:
        raise RuntimeError(
            f"RouteStack did not return a token: {data}"
        )

    return data["token"]

def create_flight_session():
    token = get_access_token()

    response = requests.post(
        f"{BASE_URL}/mcp/flight/session",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def search_locations(term):
    token = get_access_token()

    response = requests.post(
        f"{BASE_URL}/mcp/flight/locations",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "term": term,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()