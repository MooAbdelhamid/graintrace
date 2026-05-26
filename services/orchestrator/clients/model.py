import requests

PREPROCESS_URL = "http://127.0.0.1:8003/infer"


def model_call(content, filename, content_type):

    files = {"file": (filename, content, content_type)}
    data = {"source": "orchestrator"}

    response = requests.post(PREPROCESS_URL, files=files)
    return response.content
