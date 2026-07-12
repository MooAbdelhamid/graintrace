import requests

RETRIEVAL_STORE_URL = "http://127.0.0.1:8004/store"
RETRIEVAL_SEARCH_URL = "http://127.0.0.1:8004/search"
RETRIEVAL_DELETE_URL = "http://127.0.0.1:8004/delete"

# RETRIEVAL_STORE_URL = "http://127.0.0.1:6333/store"
# RETRIEVAL_SEARCH_URL = "http://127.0.0.1:6333/search"
# RETRIEVAL_DELETE_URL = "http://127.0.0.1:6333/delete"


def retrieval_store(bow_id: str, embedding: list[float], threshold: float = 0.3):
    payload = {"bow_id": bow_id, "embedding": embedding, "threshold": threshold}

    response = requests.post(RETRIEVAL_STORE_URL, json=payload)

    response.raise_for_status()
    return response.json()


def retrieval_search(embedding: list[float], top_k: int = 3):
    payload = {"embedding": embedding, "top_k": top_k}

    response = requests.post(RETRIEVAL_SEARCH_URL, json=payload)

    response.raise_for_status()
    return response.json()


def retrieval_delete(bow_id: str):

    response = requests.delete(f"{RETRIEVAL_DELETE_URL}/{bow_id}")

    response.raise_for_status()
    return response.json()
