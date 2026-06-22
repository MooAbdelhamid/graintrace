import requests

MODEL_URL = "http://127.0.0.1:8003/infer"


def model_call(content: bytes, data: dict):
    filename = data["filename"]
    content_type = data["type"]

    files = {"file": (filename, content, content_type)}

    response = requests.post(MODEL_URL, files=files)

    return response.content
