import os
from qdrant_client import QdrantClient, models

def get_qdrant_client() -> QdrantClient:
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_cluster_url = os.getenv("QDRANT_CLUSTER_URL")

    if not qdrant_api_key or not qdrant_cluster_url:
        raise ValueError("QDRANT_API_KEY and QDRANT_CLUSTER_URL must be set in environment variables")

    client = QdrantClient(
        url=qdrant_cluster_url,
        api_key=qdrant_api_key,
    )
    return client