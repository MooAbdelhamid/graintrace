import requests

RETRIEVAL_STORE_URL = "http://127.0.0.1:8004/store"
RETRIEVAL_SEARCH_URL = "http://127.0.0.1:8004/search"
RETRIEVAL_DELETE_URL = "http://127.0.0.1:8004/delete"

def retrieval_store(bow_id: str, embedding: list[float]):
    payload = {
        "bow_id": bow_id,
        "embedding": embedding,
    }

    response = requests.post(RETRIEVAL_STORE_URL, json=payload)

    response.raise_for_status()
    return response.json()

def retrieval_search(embedding: list[float], top_k: int = 3):
    payload = {
        "embedding": embedding,
        "top_k": top_k,
    }

    response = requests.post(RETRIEVAL_SEARCH_URL, json=payload)

    response.raise_for_status()
    return response.json()