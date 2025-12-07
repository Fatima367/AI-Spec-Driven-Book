from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class DocumentChunk(BaseModel):
    """
    A segment of the textbook content, typically Markdown, tokenized and embedded.
    """
    page_content: str
    chapter_title: str
    url_slug: str
    embedding: Optional[List[float]] = None  # Vector representation of the content
    doc_id: Optional[str] = None  # Unique identifier for the document
    chunk_id: Optional[str] = None  # Unique identifier for the chunk
    score: Optional[float] = None  # Similarity score from Qdrant

    class Config:
        # Allow extra fields for flexibility with Qdrant payload
        extra = "allow"


class UserQuery(BaseModel):
    """
    The natural language question submitted by the user to the chatbot.
    """
    query: str
    user_id: Optional[str] = None
    selected_text: Optional[str] = None  # Specific text highlighted by user to narrow context


class Citation(BaseModel):
    """
    A citation that links to the source of information in the response.
    """
    doc_id: str
    chunk_id: str
    url: str
    chapter_title: Optional[str] = None
    text_preview: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response from the chatbot with answer and citations.
    """
    answer: str
    citations: List[Citation] = []
    query_id: Optional[str] = None
    timestamp: Optional[str] = None


class QueryResponse(BaseModel):
    """
    Response from the direct query endpoint.
    """
    page_content: str
    chapter_title: str
    url_slug: str
    score: Optional[float] = None  # Similarity score from Qdrant


class IngestionResponse(BaseModel):
    """
    Response from the ingestion endpoint.
    """
    message: str
    documents_ingested: int
    chunks_created: int
    processing_time: Optional[float] = None