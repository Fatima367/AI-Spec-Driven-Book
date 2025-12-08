from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os
import glob
from typing import List

from ..services.embedding_service import get_embeddings
from ..services.qdrant_service import get_qdrant_client
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

# Define Pydantic models for Document Chunk
class DocumentChunk(BaseModel):
    page_content: str = Field(..., max_length=5000) # Assuming ~4 chars per token, 1200 tokens ~ 4800 chars
    chapter_title: str
    url_slug: str

    class Config:
        schema_extra = {
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
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config={"size": 3072, "distance": "Cosine"} # Placeholder for vector size, needs to match embedding model output
        )


        for file_path in markdown_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"Warning: Skipping empty file {file_path}")
                continue

            # Placeholder for actual chunking logic
            # For now, we'll treat the whole file as one chunk, or split by a simple delimiter
            # This needs to be replaced with a proper Markdown/text splitter
            chunks = content.split('\n\n') # Simple split by double newline for now

            for i, chunk_content in enumerate(chunks):
                chunk_content_stripped = chunk_content.strip()
                if not chunk_content_stripped:
                    continue

                if len(chunk_content_stripped) > 5000: # Enforce max_length for content (rough character count)
                    print(f"Warning: Chunk in {file_path} exceeds max length (5000 chars) and will be truncated. Consider more robust chunking. Chunk content: {chunk_content_stripped[:200]}...")
                    chunk_content_stripped = chunk_content_stripped[:5000] # Simple truncation

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

                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=[
                        {
                            "id": f"{url_slug}-{i}", # Unique ID for each chunk
                            "vector": embedding,
                            "payload": document_chunk.dict()
                        }
                    ]
                )
                ingested_documents_count += 1


        return {"message": "Ingestion process completed successfully.", "documents_ingested": ingested_documents_count}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))