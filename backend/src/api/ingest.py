from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os
import glob
import uuid
from typing import List

from ..services.embedding_service import get_embeddings
from ..services.qdrant_service import get_qdrant_client
from dotenv import load_dotenv

load_dotenv()

CHUNK_MAX_LENGTH = 5000 # Define a constant for max chunk length (temporarily increased for debugging)

router = APIRouter()

# Define Pydantic models for Document Chunk
class DocumentChunk(BaseModel):
    page_content: str = Field(..., max_length=CHUNK_MAX_LENGTH) # Reduced from 5000 to 1500 for better performance and context
    chapter_title: str
    url_slug: str

    class Config:
        json_schema_extra = {
            "example": {
                "page_content": "This is a chunk of text.",
                "chapter_title": "Introduction",
                "url_slug": "/docs/intro"
            }
        }

@router.post("/ingest")
async def ingest_docs():
    """
    Scrapes the Docusaurus `docs/` folder, chunks text, generates embeddings,
    and uploads to Qdrant.
    """
    try:
        # Determine the project root directory (two levels up from this file: backend/src/api/)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construct the docs path relative to project root - FIX APPLIED - VERSION 2
        # docs_path = os.path.join(project_root, "book_frontend", "docs")
        docs_path = "/mnt/c/Users/dell/Desktop/AI-Spec-Driven-Book/book_frontend/docs"

        if not os.path.exists(docs_path):
            raise HTTPException(status_code=404, detail=f"Docusaurus docs path not found at {docs_path}")

        markdown_files = []
        for root, _, files in os.walk(docs_path):
            for file in files:
                if file.endswith((".md", ".mdx")):
                    markdown_files.append(os.path.join(root, file))

        if not markdown_files:
            raise HTTPException(status_code=404, detail="No Markdown or MDX files found in Docusaurus docs.")

        ingested_documents_count = 0
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks" # Define a collection name

        # Ensure collection exists
        if not qdrant_client.collection_exists(collection_name=collection_name):
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config={"size": 3072, "distance": "Cosine"} # Placeholder for vector size, needs to match embedding model output
            )

        batch_size = 100 # Define a batch size for upserts
        points_to_upsert = []

        for file_path in markdown_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"Warning: Skipping empty file {file_path}")
                continue

            # Improved chunking logic with smaller, more manageable chunks
            # Split by paragraphs first, then ensure each chunk is under the character limit
            chunks = []
            paragraphs = content.split('\n\n')

            # Create chunks that are smaller and more context-aware, respecting CHUNK_MAX_LENGTH
            current_chunk = ""
            for paragraph in paragraphs:
                # If a single paragraph is too long, split it further into CHUNK_MAX_LENGTH pieces
                while len(paragraph) > CHUNK_MAX_LENGTH:
                    sub_chunk = paragraph[0:CHUNK_MAX_LENGTH]
                    chunks.append(sub_chunk.strip())
                    paragraph = paragraph[CHUNK_MAX_LENGTH:]

                # After handling overly long paragraphs, add to current_chunk or append as new
                # Ensure current_chunk + paragraph does not exceed CHUNK_MAX_LENGTH
                if len(current_chunk) + len(paragraph) + 2 > CHUNK_MAX_LENGTH and current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph

            # Don't forget the last chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            for i, chunk_content in enumerate(chunks):
                chunk_content_stripped = chunk_content.strip()
                if not chunk_content_stripped:
                    continue

                # Derive metadata from file_path and chunk_content
                relative_path = os.path.relpath(file_path, docs_path)
                # Example: intro.md -> /intro
                # part1/chapter1.1.md -> /part1/chapter1.1
                url_slug = "/" + os.path.splitext(relative_path)[0].replace("\\", "/")
                
                # Basic title extraction (first heading or filename)
                chapter_title = os.path.basename(file_path).replace(".md", "").replace(".mdx", "")
                if chunk_content_stripped.startswith("#"):
                    chapter_title = chunk_content_stripped.split('\n')[0].replace("#", "").strip()

                document_chunk = DocumentChunk(
                    page_content=chunk_content_stripped,
                    chapter_title=chapter_title,
                    url_slug=url_slug
                )

                embedding = get_embeddings(document_chunk.page_content)

                point_id = str(uuid.uuid4())  # Generate a proper UUID for Qdrant

                points_to_upsert.append(
                    {
                        "id": point_id, # Unique ID for each chunk (UUID format for Qdrant)
                        "vector": embedding,
                        "payload": document_chunk.dict()
                    }
                )

                if len(points_to_upsert) >= batch_size:
                    qdrant_client.upsert(
                        collection_name=collection_name,
                        points=points_to_upsert
                    )
                    ingested_documents_count += len(points_to_upsert)
                    points_to_upsert = [] # Reset the batch
        
        # Upsert any remaining points
        if points_to_upsert:
            qdrant_client.upsert(
                collection_name=collection_name,
                points=points_to_upsert
            )
            ingested_documents_count += len(points_to_upsert)



        return {"message": "Ingestion process completed successfully.", "documents_ingested": ingested_documents_count}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))