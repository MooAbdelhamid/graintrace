import requests

META_STORE_URL = "http://127.0.0.1:8005/store"
META_SEARCH_URL = "http://127.0.0.1:8005/search"
META_DELETE_URL = "http://127.0.0.1:8005/delete"


def meta_store(bow_id: str, maker: str, bow_kind: str, owner: str):
    payload = {"bow_id": bow_id, "maker": maker, "bow_kind": bow_kind, "owner": owner}

    response = requests.post(META_STORE_URL, params=payload)

    response.raise_for_status()
    return response.json()


def meta_search(bow_id: str):
    payload = {"bow_id": bow_id}

    response = requests.post(META_SEARCH_URL, params=payload)

    response.raise_for_status()
    return response.json()
