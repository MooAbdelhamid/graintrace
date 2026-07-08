import json
import os

import requests

from lib.schemas import Bow

ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://localhost:8001")
TIMEOUT_S = 30


def register(
    bow: Bow,
    image_bytes: bytes,
    filename: str = "bow.jpg",
    content_type: str = "image/jpeg",
) -> dict:

    files = {"file": (filename, image_bytes, content_type)}

    data = bow.model_dump(exclude_none=True)

    if data.get("materials"):
        data["materials"] = json.dumps(data["materials"])
    else:
        data.pop("materials", None)

    r = requests.post(
        f"{ORCHESTRATOR_URL}/register/",
        files=files,
        data=data,
        timeout=TIMEOUT_S,
    )

    # will need handling
    r.raise_for_status()

    return r.json()


def verify(
    image_bytes: bytes, filename: str = "query.jpg", content_type: str = "image/jpeg"
) -> dict:

    files = {"file": (filename, image_bytes, content_type)}

    r = requests.post(
        f"{ORCHESTRATOR_URL}/verify/",
        files=files,
        timeout=TIMEOUT_S,
    )

    # will need handling
    r.raise_for_status()

    return r.json()
