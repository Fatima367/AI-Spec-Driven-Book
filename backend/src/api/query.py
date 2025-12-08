from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from ..services.embedding_service import get_embeddings
from ..services.qdrant_service import get_qdrant_client
from .ingest import DocumentChunk # Reuse the DocumentChunk model
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: List[DocumentChunk]

@router.post("/query", response_model=QueryResponse)
async def query_docs(request: QueryRequest):
    """
    Retrieves relevant document chunks based on a direct query.
    """
    try:
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks" # Must match the collection name used in ingest.py

        # Check if collection exists
        if not qdrant_client.collection_exists(collection_name=collection_name):
            raise HTTPException(status_code=404, detail=f"Qdrant collection '{collection_name}' not found. Please ingest documents first.")

        query_embedding = get_embeddings(request.query)

        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5, # Limit to top 5 relevant documents
            with_payload=True # Retrieve the full payload (DocumentChunk data)
        )
        
        results = []
        for scored_point in search_result.points:
            if scored_point.payload:
                # Assuming payload directly maps to DocumentChunk attributes
                results.append(DocumentChunk(**scored_point.payload))
        
        return QueryResponse(results=results)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))