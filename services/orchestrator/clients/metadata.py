import json
from io import BytesIO

import requests
from models.bow import Bow
from PIL import Image

META_STORE_URL = "http://127.0.0.1:8005/store"
META_SEARCH_URL = "http://127.0.0.1:8005/search"
META_IMAGE_URL = "http://127.0.0.1:8005/image/"
META_DELETE_URL = "http://127.0.0.1:8005/delete"

META_LIST_ALL_URL = "http://127.0.0.1:8005/list_all"


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


def meta_delete(bow_id: str):
    payload = {"bow_id": bow_id}

    response = requests.delete(f"{META_DELETE_URL}/{bow_id}")

    response.raise_for_status()
    return response.json()


def meta_count():
    response = requests.get(META_LIST_ALL_URL)
    response.raise_for_status()

    data = response.json()
    return len(data)


def meta_last():
    response = requests.get(META_LIST_ALL_URL)
    response.raise_for_status()

    data = response.json()
    date = data[0]["registered_at"]

    return date


def meta_image(bow_id: str):
    URL = META_IMAGE_URL + bow_id

    response = requests.get(URL)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    return image
