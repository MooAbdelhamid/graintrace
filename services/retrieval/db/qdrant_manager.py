import torch
from config import config
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(
            host=config.QDRANT_HOST,
            port=config.QDRANT_PORT,
        )

        self.collection_name = config.COLLECTION_NAME
        self.embedding_dim = config.EMBEDDING_DIM

        self._init_collection()

    def _init_collection(self):
        existing = [
            collection.name for collection in self.client.get_collections().collections
        ]

        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.EUCLID,
                ),
            )

    def store(self, bow_id: str, embedding: list[float]):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=self._bow_id_to_int(bow_id),
                    vector=embedding,
                    payload={"bow_id": bow_id},
                )
            ],
        )

    import torch

    def search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=top_k,
            with_payload=True,
            with_vectors=True,  # needed for PyTorch check
        )

        query = torch.tensor(embedding, dtype=torch.float32)

        # --- PyTorch debug print ---
        for point in results.points:
            vec = torch.tensor(point.vector, dtype=torch.float32)
            dist = torch.norm(query - vec, p=2).item()

            print(
                f"[PYTORCH DEBUG] bow_id={point.payload.get('bow_id')} "
                f"euclidean_distance={dist:.6f}"
            )

        return [
            {
                "bow_id": point.payload.get("bow_id"),
                "score": point.score,
            }
            for point in results.points
        ]

    def delete(self, bow_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[self._bow_id_to_int(bow_id)],
        )

    def get_client(self) -> QdrantClient:
        return self.client

    @staticmethod
    def _bow_id_to_int(bow_id: str) -> int:
        return abs(hash(bow_id)) % (10**9)
