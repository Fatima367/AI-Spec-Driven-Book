import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, ANY
from src.main import app
import os
from dotenv import load_dotenv

load_dotenv()


# Mock the services before importing the api module to ensure mocks are in place
@pytest.fixture(autouse=True)
def mock_services():
    with patch('src.api.ingest.get_qdrant_client') as mock_get_qdrant_client, \
         patch('src.api.ingest.get_embeddings') as mock_get_embeddings:
        
        # Configure mock_get_qdrant_client
        mock_qdrant_client = MagicMock()
        mock_get_qdrant_client.return_value = mock_qdrant_client
        mock_qdrant_client.recreate_collection.return_value = None
        mock_qdrant_client.upsert.return_value = None

        # Configure mock_get_embeddings
        mock_get_embeddings.return_value = [0.1] * 3072 # Return a dummy embedding vector

        yield mock_qdrant_client, mock_get_embeddings

client = TestClient(app)

def test_ingest_docs_success(mock_services):
    """Test successful ingestion of documents."""
    mock_qdrant_client, mock_get_embeddings = mock_services

    # Create dummy Docusaurus docs structure
    test_docs_path = "book_frontend/docs"
    os.makedirs(os.path.join(test_docs_path, "part1"), exist_ok=True)
    with open(os.path.join(test_docs_path, "intro.md"), "w") as f:
        f.write("# Introduction\n\nThis is an intro paragraph.")
    with open(os.path.join(test_docs_path, "part1", "chapter1.1.md"), "w") as f:
        f.write("## Chapter 1.1\n\nContent for chapter 1.1.")

    response = client.post("/api/v1/ingest")

    assert response.status_code == 200
    assert response.json()["message"] == "Ingestion process completed successfully."
    assert response.json()["documents_ingested"] >= 2 # At least 2 documents (intro and chapter1.1)

    mock_qdrant_client.recreate_collection.assert_called_once_with(
        collection_name="book_content_chunks",
        vectors_config={"size": 3072, "distance": "Cosine"}
    )
    assert mock_get_embeddings.call_count >= 2 # Called for each chunk
    assert mock_qdrant_client.upsert.call_count >= 2 # Called for each chunk

    # Clean up dummy docs
    os.remove(os.path.join(test_docs_path, "intro.md"))
    os.remove(os.path.join(test_docs_path, "part1", "chapter1.1.md"))
    os.rmdir(os.path.join(test_docs_path, "part1"))


def test_ingest_docs_no_docs_path(mock_services):
    """Test ingestion when Docusaurus docs path does not exist."""
    # Temporarily rename/remove the docs folder for this test
    original_docs_path = "book_frontend/docs"
    temp_docs_path = "book_frontend/docs_temp_removed"
    if os.path.exists(original_docs_path):
        os.rename(original_docs_path, temp_docs_path)

    try:
        response = client.post("/api/v1/ingest")
        assert response.status_code == 404
        assert "Docusaurus docs path not found" in response.json()["detail"]
    finally:
        if os.path.exists(temp_docs_path):
            os.rename(temp_docs_path, original_docs_path)

def test_ingest_docs_no_markdown_files(mock_services):
    """Test ingestion when no markdown files are found."""
    test_docs_path = "book_frontend/docs"
    os.makedirs(test_docs_path, exist_ok=True)
    
    # Create a non-markdown file
    with open(os.path.join(test_docs_path, "image.png"), "w") as f:
        f.write("dummy image content")

    response = client.post("/api/v1/ingest")
    assert response.status_code == 404
    assert "No Markdown or MDX files found" in response.json()["detail"]

    os.remove(os.path.join(test_docs_path, "image.png"))
    os.rmdir(test_docs_path)