import json

import requests
from models.bow import Bow

META_STORE_URL = "http://127.0.0.1:8005/store"
META_SEARCH_URL = "http://127.0.0.1:8005/search"
META_DELETE_URL = "http://127.0.0.1:8005/delete"


def meta_store(
    bow: Bow,
    image_bytes: bytes,
    filename: str = "bow.jpg",
    content_type: str = "image/jpeg",
):
    files = {"file": (filename, image_bytes, content_type)}

    data = bow.model_dump(exclude_none=True)

    if data.get("materials"):
        data["materials"] = json.dumps(data["materials"])
    else:
        data.pop("materials", None)

    response = requests.post(META_STORE_URL, files=files, data=data)

    response.raise_for_status()
    return response.json()


def meta_search(bow_id: str):
    payload = {"bow_id": bow_id}

    response = requests.post(META_SEARCH_URL, params=payload)

    response.raise_for_status()
    return response.json()
