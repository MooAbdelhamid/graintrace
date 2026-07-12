import json
import os
from io import BytesIO

import requests
from PIL import Image

from lib.schemas import Bow

ORCHESTRATOR_URL = os.environ.get(
    "ORCHESTRATOR_URL", "http://localhost:8001"
)  # changed from "http://localhost:8001"


META_IMAGE_URL = "http://127.0.0.1:8005/image/"


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

    r = requests.post(f"{ORCHESTRATOR_URL}/register/", files=files, data=data)

    # will need handling

    print(r.status_code)
    print(r.text)
    r.raise_for_status()

    return r.json()


def verify(
    image_bytes: bytes, filename: str = "query.jpg", content_type: str = "image/jpeg"
) -> dict:

    files = {"file": (filename, image_bytes, content_type)}

    r = requests.post(f"{ORCHESTRATOR_URL}/verify/", files=files)

    # will need handling

    r.raise_for_status()

    return r.json()


def delete(
    bow_id: str,
) -> dict:

    data = {"bow_id": bow_id}

    r = requests.delete(f"{ORCHESTRATOR_URL}/delete/{bow_id}", data=data)
    # print("received at client")
    # will need handling

    r.raise_for_status()

    return r.json()


def get_stats() -> dict:
    r = requests.get(f"{ORCHESTRATOR_URL}/stats")

    r.raise_for_status()

    return r.json()


def health_check() -> dict:
    services = {
        "orchestrator": f"{ORCHESTRATOR_URL}/health",
        "preprocessing": "http://localhost:8002/health",
        "model": "http://localhost:8003/health",
        "retrieval": "http://localhost:8004/health",
        "metadata": "http://localhost:8005/health",
    }

    result = {}

    for name, url in services.items():
        try:
            r = requests.get(url, timeout=2)
            result[name] = r.status_code == 200
        except requests.RequestException:
            result[name] = False

    return result


def meta_image(bow_id: str):
    URL = META_IMAGE_URL + bow_id

    response = requests.get(URL)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    return image
