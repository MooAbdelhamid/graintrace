import requests

PREPROCESS_URL = "http://127.0.0.1:8002/preprocess"


def preprocessing_call(content, data):
    filename = data["filename"]
    content_type = data["type"]

    files = {"file": (filename, content, content_type)}

    response = requests.post(PREPROCESS_URL, files=files)
    return response.content
