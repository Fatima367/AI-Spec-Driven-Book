import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any

# Import your existing services and models
from services.embedding_service import get_embeddings
from services.qdrant_service import get_qdrant_client
from models import DocumentChunk as DocumentChunkModel


def handler(event, context):
    """
    Netlify Function handler for ingest endpoint
    """
    start_time = datetime.now()
    try:
        # Determine docs path - adjust as needed for your deployment
        docs_path = os.path.join(os.getcwd(), "..", "..", "book_frontend", "docs")
        if not os.path.exists(docs_path):
            # Try alternative path structure
            docs_path = os.path.join(os.getcwd(), "..", "book_frontend", "docs")
            if not os.path.exists(docs_path):
                # Try another alternative
                docs_path = os.path.join(os.getcwd(), "book_frontend", "docs")
                if not os.path.exists(docs_path):
                    return {
                        'statusCode': 404,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'POST, OPTIONS',
                            'Access-Control-Allow-Headers': 'Content-Type'
                        },
                        'body': json.dumps({'error': f"Docusaurus docs path not found at expected locations"})
                    }

        markdown_files = []
        for root, _, files in os.walk(docs_path):
            for file in files:
                if file.endswith((".md", ".mdx")):
                    markdown_files.append(os.path.join(root, file))

        if not markdown_files:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': "No Markdown or MDX files found in Docusaurus docs."})
            }

        total_chunks_created = 0
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        # Determine embedding size by creating a test embedding
        test_embedding = get_embeddings("test")
        embedding_size = len(test_embedding)

        # Ensure collection exists with correct vector size
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config={"size": embedding_size, "distance": "Cosine"}  # Match embedding model output
        )

        for file_path in markdown_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"Warning: Skipping empty file {file_path}")
                continue

            # Simple chunking by paragraphs with size limits
            # Split content into chunks by double newlines first
            potential_chunks = content.split('\n\n')

            # Further split large chunks to keep them under size limits
            actual_chunks = []
            for chunk in potential_chunks:
                if len(chunk) <= 2000:  # Keep chunks reasonably sized
                    actual_chunks.append(chunk)
                else:
                    # If chunk is too large, split it by sentences
                    sentences = chunk.split('. ')
                    current_chunk = ""
                    for sentence in sentences:
                        if len(current_chunk + sentence) < 1500:
                            current_chunk += sentence + ". "
                        else:
                            if current_chunk:
                                actual_chunks.append(current_chunk.strip())
                            current_chunk = sentence + ". "
                    if current_chunk:
                        actual_chunks.append(current_chunk.strip())

            for i, chunk_content in enumerate(actual_chunks):
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
                # Extract title from markdown heading if present
                lines = chunk_content_stripped.split('\n')
                for line in lines:
                    if line.strip().startswith('#'):
                        chapter_title = line.strip().replace('#', '').strip()
                        break

                # Create document chunk with unique IDs
                doc_chunk = DocumentChunkModel(
                    page_content=chunk_content_stripped,
                    chapter_title=chapter_title,
                    url_slug=url_slug,
                    doc_id=os.path.basename(file_path).replace(".md", "").replace(".mdx", ""),
                    chunk_id=str(uuid.uuid4())  # Generate unique chunk ID
                )

                embedding = get_embeddings(doc_chunk.page_content)

                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=[
                        {
                            "id": doc_chunk.chunk_id,  # Use UUID for unique ID
                            "vector": embedding,
                            "payload": doc_chunk.dict()
                        }
                    ]
                )
                total_chunks_created += 1

        processing_time = (datetime.now() - start_time).total_seconds()

        response = {
            "message": "Ingestion process completed successfully.",
            "documents_ingested": len(markdown_files),
            "chunks_created": total_chunks_created,
            "processing_time": processing_time
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response)
        }

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }