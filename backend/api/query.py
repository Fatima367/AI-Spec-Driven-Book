from fastapi import APIRouter, HTTPException
from typing import List

from models import DocumentChunk
from services.embedding_service import get_embeddings
from services.qdrant_service import get_qdrant_client

router = APIRouter()


@router.post("/query", response_model=List[DocumentChunk])
async def query_docs(query: str):
    """
    Retrieves relevant document chunks based on a direct query.
    """
    try:
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks" # Must match the collection name used in ingest.py

        # Check if collection exists
        if not qdrant_client.collection_exists(collection_name=collection_name):
            raise HTTPException(status_code=404, detail=f"Qdrant collection '{collection_name}' not found. Please ingest documents first.")

        query_embedding = get_embeddings(query)

        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5, # Limit to top 5 relevant documents
            with_payload=True # Retrieve the full payload (DocumentChunk data)
        )

        results = []
        for scored_point in search_result.points:
            if scored_point.payload:
                # Create DocumentChunk from payload and add score
                chunk_data = scored_point.payload.copy()
                chunk_data['score'] = scored_point.score
                results.append(DocumentChunk(**chunk_data))

        return results

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
