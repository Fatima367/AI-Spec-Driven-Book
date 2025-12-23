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
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # Construct the docs path relative to project root
        docs_path = os.path.join(project_root, "book_frontend", "docs")

        if not os.path.exists(docs_path):
            raise HTTPException(status_code=404, detail=f"Docusaurus docs path not found at {docs_path}")

        markdown_files = []
        for root, _, files in os.walk(docs_path):
            for file in files:
                if file.endswith((".md", ".mdx")):
                    markdown_files.append(os.path.join(root, file))

        if not markdown_files:
            raise HTTPException(status_code=404, detail="No Markdown or MDX files found in Docusaurus docs.")

        all_chunks = []
        for file_path in markdown_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"Warning: Skipping empty file {file_path}")
                continue

            chunks = []
            paragraphs = content.split('\n\n')

            current_chunk = ""
            for paragraph in paragraphs:
                while len(paragraph) > CHUNK_MAX_LENGTH:
                    sub_chunk = paragraph[0:CHUNK_MAX_LENGTH]
                    chunks.append(sub_chunk.strip())
                    paragraph = paragraph[CHUNK_MAX_LENGTH:]

                if len(current_chunk) + len(paragraph) + 2 > CHUNK_MAX_LENGTH and current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph

            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            for chunk_content in chunks:
                chunk_content_stripped = chunk_content.strip()
                if not chunk_content_stripped:
                    continue

                relative_path = os.path.relpath(file_path, docs_path)
                url_slug = "/" + os.path.splitext(relative_path)[0].replace("\\", "/")
                
                chapter_title = os.path.basename(file_path).replace(".md", "").replace(".mdx", "")
                if chunk_content_stripped.startswith("#"):
                    chapter_title = chunk_content_stripped.split('\n')[0].replace("#", "").strip()

                all_chunks.append(DocumentChunk(
                    page_content=chunk_content_stripped,
                    chapter_title=chapter_title,
                    url_slug=url_slug
                ))
        
        if not all_chunks:
            return {"message": "No content to ingest.", "documents_ingested": 0}

        texts_to_embed = [chunk.page_content for chunk in all_chunks]
        embeddings = get_embeddings(texts_to_embed)

        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"
        vector_size = len(embeddings[0])

        if qdrant_client.collection_exists(collection_name=collection_name):
            collection_info = qdrant_client.get_collection(collection_name=collection_name)
            # This needs to be adapted if you use named vectors
            if collection_info.config.params.vectors.size != vector_size:
                qdrant_client.delete_collection(collection_name=collection_name)
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config={"size": vector_size, "distance": "Cosine"}
                )
        else:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config={"size": vector_size, "distance": "Cosine"}
            )

        points_to_upsert = []
        for i, chunk in enumerate(all_chunks):
            point_id = str(uuid.uuid4())
            points_to_upsert.append(
                {
                    "id": point_id,
                    "vector": embeddings[i],
                    "payload": chunk.dict()
                }
            )

        batch_size = 100
        ingested_documents_count = 0
        for i in range(0, len(points_to_upsert), batch_size):
            batch = points_to_upsert[i:i + batch_size]
            qdrant_client.upsert(
                collection_name=collection_name,
                points=batch
            )
            ingested_documents_count += len(batch)

        return {"message": "Ingestion process completed successfully.", "documents_ingested": ingested_documents_count}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
