from config import config
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
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

    def search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=top_k,
            with_payload=True,
            with_vectors=True,  # needed for PyTorch check
        )

        return [
            {
                "bow_id": point.payload.get("bow_id"),
                "score": point.score,
            }
            for point in results.points
        ]

    def search_by_id(self, bow_id: str) -> dict | None:
        # fetch a single point by bow_id from the payload
        # uses scroll with a filter instead of get() since we store bow_id in payload not as qdrant id
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[FieldCondition(key="bow_id", match=MatchValue(value=bow_id))]
            ),
            with_payload=True,
            with_vectors=True,
            limit=1,
        )
        points = results[0]
        if not points:
            return None
        return {
            "bow_id": points[0].payload.get("bow_id"),
            "embedding": points[0].vector,
        }

    def check_before_adding(
        self, embedding: list[float], threshold: float
    ) -> dict | None:
        # separate function that can be used as a flag before store()
        # returns the closest match if score is above threshold, None if safe to add
        results = self.search(embedding, top_k=1)
        if not results:
            return None
        top = results[0]
        if top["score"] <= threshold:
            return top  # similar bow already exists
        return None  # safe to add

    def delete(self, bow_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[self._bow_id_to_int(bow_id)],
        )

    def delete_all(self) -> None:
        # deletes the collection and recreates it empty
        self.client.delete_collection(collection_name=self.collection_name)
        self._init_collection()

    def get_client(self) -> QdrantClient:
        return self.client

    @staticmethod
    def _bow_id_to_int(bow_id: str) -> int:
        return abs(hash(bow_id)) % (10**9)
