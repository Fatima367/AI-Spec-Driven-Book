import os
import pytest
from unittest.mock import MagicMock, patch
from services.embedding_service import get_gemini_embedding_client, get_embeddings
from openai import OpenAI
from openai.types import CreateEmbeddingResponse, Embedding

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_gemini_embedding_client_success():
    """Test successful Gemini embedding client initialization."""
    client = get_gemini_embedding_client()
    assert isinstance(client, OpenAI)
    assert client.api_key == "test_gemini_key"
    assert client.base_url == "https://generativelanguage.googleapis.com/v1beta/openai/"

@patch.dict(os.environ, {"GEMINI_API_KEY": ""})
def test_get_gemini_embedding_client_no_api_key():
    """Test Gemini embedding client initialization without API key."""
    with pytest.raises(ValueError, match="GEMINI_API_KEY must be set in environment variables"):
        get_gemini_embedding_client()

@patch('services.embedding_service.get_gemini_embedding_client')
@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_embeddings_success(mock_get_client):
    """Test successful embedding generation."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    # Mock the response from client.embeddings.create
    mock_embedding = Embedding(embedding=[0.1, 0.2, 0.3], index=0, object="embedding")
    mock_response = CreateEmbeddingResponse(data=[mock_embedding], model="embedding-001", object="list")
    mock_client.embeddings.create.return_value = mock_response

    text = "test text"
    embeddings = get_embeddings(text)

    mock_get_client.assert_called_once()
    mock_client.embeddings.create.assert_called_once_with(input=text, model="embedding-001")
    assert embeddings == [0.1, 0.2, 0.3]

@patch('services.embedding_service.get_gemini_embedding_client')
@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_embeddings_api_error(mock_get_client):
    """Test embedding generation with API error."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.embeddings.create.side_effect = Exception("API Error")

    text = "test text"
    with pytest.raises(Exception, match="API Error"):
        get_embeddings(text)

    mock_get_client.assert_called_once()
    mock_client.embeddings.create.assert_called_once_with(input=text, model="embedding-001")