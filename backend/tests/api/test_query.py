import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, ANY
from main import app # Assuming main.py is in the same directory as this test file

# Mock the services before importing the api module to ensure mocks are in place
@pytest.fixture(autouse=True)
def mock_services():
    with patch('api.query.get_qdrant_client') as mock_get_qdrant_client, \
         patch('api.query.get_embeddings') as mock_get_embeddings:
        
        # Configure mock_get_qdrant_client
        mock_qdrant_client = MagicMock()
        mock_get_qdrant_client.return_value = mock_qdrant_client
        mock_qdrant_client.collection_exists.return_value = True

        # Mock search_result
        mock_point = MagicMock()
        mock_point.payload = {
            "page_content": "Relevant content",
            "chapter_title": "Test Chapter",
            "url_slug": "/docs/test-chapter"
        }
        mock_point.id = "test-id-0" # Assign an ID
        
        mock_search_result = MagicMock()
        mock_search_result.points = [mock_point]
        mock_qdrant_client.query.return_value = mock_search_result

        # Configure mock_get_embeddings
        mock_get_embeddings.return_value = [0.1] * 3072 # Return a dummy embedding vector

        yield mock_qdrant_client, mock_get_embeddings

client = TestClient(app)

def test_query_docs_success(mock_services):
    """Test successful querying of documents."""
    mock_qdrant_client, mock_get_embeddings = mock_services
    
    response = client.post(
        "/api/v1/query",
        json={"query": "What is RAG?"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["page_content"] == "Relevant content"
    assert response.json()["results"][0]["chapter_title"] == "Test Chapter"
    assert response.json()["results"][0]["url_slug"] == "/docs/test-chapter"

    mock_get_embeddings.assert_called_once_with("What is RAG?")
    mock_qdrant_client.collection_exists.assert_called_once_with(collection_name="book_content_chunks")
    mock_qdrant_client.query.assert_called_once_with(
        collection_name="book_content_chunks",
        query_vector=[0.1] * 3072,
        limit=5,
        with_payload=True
    )

def test_query_docs_collection_not_found(mock_services):
    """Test querying when the Qdrant collection does not exist."""
    mock_qdrant_client, _ = mock_services
    mock_qdrant_client.collection_exists.return_value = False # Simulate collection not found

    response = client.post(
        "/api/v1/query",
        json={"query": "What is RAG?"}
    )

    assert response.status_code == 404
    assert "collection 'book_content_chunks' not found" in response.json()["detail"]
    mock_qdrant_client.collection_exists.assert_called_once_with(collection_name="book_content_chunks")
    mock_qdrant_client.query.assert_not_called()