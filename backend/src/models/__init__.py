from pydantic import BaseModel
from typing import Optional, List
from typing import Any, Dict


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


class UserQuery(BaseModel):
    """
    The natural language question submitted by the user to the chatbot.
    """
    query: str
    user_id: Optional[str] = None
    selected_text: Optional[str] = None  # Specific text highlighted by user to narrow context


class ChatResponse(BaseModel):
    """
    Response from the chatbot with answer and citations.
    """
    answer: str
    citations: List[Dict[str, Any]]  # List of citations with doc_id, chunk_id, url


class QueryResponse(BaseModel):
    """
    Response from the direct query endpoint.
    """
    page_content: str
    chapter_title: str
    url_slug: str